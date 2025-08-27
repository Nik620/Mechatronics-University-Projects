/*****************************************************************************
*   File:     130000-IN-S.cpp
*   Version:  0.0.3
*   Project:  Prepreg Printer Control System
*   Date:     2025-08-08
*   Description: This file contains the main function for the Prepreg Printer
*              Control System. It initializes the system, sets up the user 
*              interface, and starts the main event loop.
*****************************************************************************/

/********** Libraries *******************************************************/
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "pico/time.h"

/********** Pin Definitions *************************************************/
#define DRIVER_DIR      0     // GP0 -> 2977 driver DIR
#define DRIVER_STEP     1     // GP1 -> 2977 driver STEP
#define DRIVER_ENABLE   5     // GP5 -> 2977 driver ENABLE (will determine if needed)
#define DIAL            28    // GP28 -> potentiometer
#define FAN             2     // GP2 -> Fan
#define PUMP            3     // GP3 -> Pump
#define OPTO            27     // GP27 -> Opto-isolator (for external control)
#define DEBUG_LED_PIN   PICO_DEFAULT_LED_PIN

/********** Constants *******************************************************/
// Constants for the stepper motor and RPM calculations
// The number of microsteps affects smoothness and maximum speed.
// Higher microsteps = smoother motion, but lower maximum speed.
// Lower microsteps = jerkier motion, but higher maximum speed.
const int base_steps_per_rev = 200;       // 1.8° stepper motor
const int microsteps = 4;                 // 2977 driver microstepping
const float gear_ratio = 1.0f;            // 1:1, will adjust later for output
const int steps_per_rev_wheel = base_steps_per_rev * microsteps * gear_ratio;

// Constants for the dial to RPM mapping
// Increased the maximum RPM to give a much wider range.
// The maximum speed you can achieve is also dependent on the motor and voltage.
const int dial_adc_min = 0; // Minimum ADC value for the dial
const int dial_adc_max = 4095; // Maximum ADC value for the dial
const float rpm_min = -8.0f; // Minimum RPM (negative for reverse)
const float rpm_max = 50.0f; // Maximum RPM (positive for forward)


/********** Main Routine ****************************************************/
int main() {
    stdio_init_all();

    // Initialize GPIOs
    gpio_init(DRIVER_DIR);
    gpio_set_dir(DRIVER_DIR, GPIO_OUT);

    gpio_init(DRIVER_STEP);
    gpio_set_dir(DRIVER_STEP, GPIO_OUT);

    // Initialize and set GP5 for the DRIVER_ENABLE pin
    // Setting it to LOW enables the 2977 driver
    gpio_init(DRIVER_ENABLE);
    gpio_set_dir(DRIVER_ENABLE, GPIO_OUT);
    gpio_put(DRIVER_ENABLE, 0); // LOW signal to enable the driver

    // Initialize the fan and pump control pins
    gpio_init(FAN);
    gpio_set_dir(FAN, GPIO_OUT);
    gpio_put(FAN, 0); // Turn off fan initially

    gpio_init(PUMP);
    gpio_set_dir(PUMP, GPIO_OUT);
    gpio_put(PUMP, 0); // Turn off pump initially

    // Initialize the opto-isolator pin
    //gpio_init(OPTO);
    //gpio_set_dir(OPTO, GPIO_IN);

    // Initialize the debug LED pin
    // This will be used for debugging and status indication
    gpio_init(DEBUG_LED_PIN);
    gpio_set_dir(DEBUG_LED_PIN, GPIO_OUT);

    // Initialize ADC for GP28 (ADC2)
    adc_init();
    adc_gpio_init(DIAL);
    adc_select_input(2);  // ADC2 = GP28

    // Variables for the independent LED blink timer
    absolute_time_t led_timer_last_toggle = get_absolute_time();
    int led_blink_interval_ms = 1000; // Blink every 1000 ms (1 second)

    // Main event loop
    // This loop will read the dial, control the motor direction and speed,
    // and toggle the debug LED at a fixed interval.
    // It will also read the opto-isolator, fan, and control the pump.
    while (true) {
        // Motor Control Logic
        // Read the dial value from the ADC and convert to RPM
        uint16_t dial_value = adc_read(); // Read the dial (0 to 4095)
        float rpm = ((float)dial_value / 4095.0f)*(rpm_max - rpm_min)+rpm_min; 
        if (rpm >= 0) {
            gpio_put(DRIVER_DIR, 1);
        } else {
            gpio_put(DRIVER_DIR, 0);
            rpm = -rpm;  // Make it positive for timing
        }

        // Calculate steps per second and delay between steps
        float steps_per_sec = (steps_per_rev_wheel * rpm) / 60.0f;
        if (steps_per_sec < 0.5f) {
            // Too slow to step – idle
            sleep_ms(10);
        } else {
            uint delay_us = (uint)(1000000.0f / steps_per_sec);
            // Generate step pulse
            gpio_put(DRIVER_STEP, 1);
            sleep_us(2);
            gpio_put(DRIVER_STEP, 0);
            sleep_us(delay_us - 2);  
        }


        // Pump Control Logic
        // Enable the pump if the motor is in the forward direction
        if (rpm > 0) {
            gpio_put(PUMP, 1); // Turn on pump
        } else {
            gpio_put(PUMP, 0); // Turn off pump
        }
        // Read the opto-isolator (if used)
        // int opto_value = gpio_get(OPTO); 
        // if (opto_value) {
        //     gpio_put(PUMP, 1); // Turn on pump if opto is high
        // } else { 
        //     gpio_put(PUMP, 0); // Turn off pump if opto is low
        // }


        // Fan Control Logic
        // Enable the fan when the motor is running
        if (rpm != 0) {
            gpio_put(FAN, 1); // Turn on fan
        } else {
            gpio_put(FAN, 0); // Turn off fan
        }


        // Debug LED Blinking Logic
        // This will indicate that the system is running and processing
        // Toggle the debug LED every led_blink_interval_ms milliseconds
        if (absolute_time_diff_us(led_timer_last_toggle, get_absolute_time()) >= led_blink_interval_ms * 1000) {
            gpio_xor_mask(1 << DEBUG_LED_PIN);
            led_timer_last_toggle = get_absolute_time();
        }

    }

    return 0;  // Return in case of exit, but shouldn't reach here
}
