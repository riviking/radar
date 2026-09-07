#include <Servo.h>

// ======================================================
// PINS
// ======================================================

#define TRIG_PIN 7
#define ECHO_PIN 8
#define SERVO_PIN 9

// ======================================================
// RADAR SETTINGS
// ======================================================

#define MIN_DISTANCE 2
#define MAX_DISTANCE 200

#define MIN_ANGLE 0
#define MAX_ANGLE 90

// ======================================================
// SERVO
// ======================================================

Servo radarServo;

int angle = 0;
int direction = 1;

// ======================================================
// ONE RAW HC-SR04 READING
// ======================================================

float readOnce()
{
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(3);

    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);

    digitalWrite(TRIG_PIN, LOW);

    // 2 m range -> need longer timeout
    unsigned long duration =
        pulseIn(ECHO_PIN, HIGH, 25000);

    // No echo
    if (duration == 0)
    {
        return MAX_DISTANCE;
    }

    float distance =
        duration * 0.0343 / 2.0;

    // Invalid distance
    if (distance < MIN_DISTANCE)
    {
        return MAX_DISTANCE;
    }

    if (distance > MAX_DISTANCE)
    {
        return MAX_DISTANCE;
    }

    return distance;
}

// ======================================================
// MEDIAN FILTER
// ======================================================

float getDistance()
{
    float readings[5];

    for (int i = 0; i < 5; i++)
    {
        readings[i] = readOnce();

        delay(3);
    }

    // Sort
    for (int i = 0; i < 4; i++)
    {
        for (int j = i + 1; j < 5; j++)
        {
            if (readings[j] < readings[i])
            {
                float temp = readings[i];

                readings[i] = readings[j];

                readings[j] = temp;
            }
        }
    }

    // Median
    return readings[2];
}

// ======================================================
// SETUP
// ======================================================

void setup()
{
    Serial.begin(115200);

    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    radarServo.attach(SERVO_PIN);

    radarServo.write(0);

    delay(1000);
}

// ======================================================
// MAIN LOOP
// ======================================================

void loop()
{
    // Move servo
    radarServo.write(angle);

    // Servo settle time
    if (direction == 1)
    {
        delay(70);
    }
    else
    {
        delay(30);
    }

    // Get filtered distance
    float distance = getDistance();

    // Send:
    // angle,distance
    //
    // Example:
    // 35,123.4

    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance, 1);

    // Move next angle
    angle += direction;

    // Reached 90°
    if (angle >= MAX_ANGLE)
    {
        angle = MAX_ANGLE;

        direction = -1;
    }

    // Reached 0°
    if (angle <= MIN_ANGLE)
    {
        angle = MIN_ANGLE;

        direction = 1;
    }
}