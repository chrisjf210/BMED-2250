import serial
import time


def get_user_inputs():
    age = int(input("Enter your age: "))
    weight = float(input("Enter your weight (in pounds): "))
    height = float(input("Enter your height (in inches): "))
    diabetes_type = input("Do you have Type 1, Type 2, or no diabetes? (T1/T2/NONE): ").strip().upper()

    return age, weight, height, diabetes_type


def connect_to_arduino(port='COM3', baud_rate=9600):
    """
    Opens serial connection to Arduino.
    Change COM3 to the correct port on your computer.
    """
    ser = serial.Serial(port, baud_rate, timeout=2)
    time.sleep(2)  # gives Arduino time to reset after connection
    return ser


def get_sensor_data(ser):
    line = ser.readline().decode('utf-8').strip()

    if not line:
        raise ValueError("No data received from Arduino.")

    parts = line.split(',')

    if len(parts) != 2:
        raise ValueError(f"Unexpected data format: {line}")

    heart_rate = int(parts[0])
    blood_oxygen = int(parts[1])

    return heart_rate, blood_oxygen


def get_heart_rate_zone(age, heart_rate):
    max_heart_rate = 220 - age
    moderate_low = 0.50 * max_heart_rate
    moderate_high = 0.70 * max_heart_rate
    vigorous_high = 0.90 * max_heart_rate

    if moderate_low <= heart_rate < moderate_high:
        zone = "Moderate Exercise"
    elif moderate_high <= heart_rate <= vigorous_high:
        zone = "Vigorous Exercise"
    else:
        zone = "Outside moderate/vigorous range"

    return max_heart_rate, moderate_low, moderate_high, vigorous_high, zone


def main():
    age, weight, height, diabetes_type = get_user_inputs()
    ser = connect_to_arduino(port='COM3', baud_rate=9600)

    try:
        heart_rate, blood_oxygen = get_sensor_data(ser)

        max_hr, mod_low, mod_high, vig_high, zone = get_heart_rate_zone(age, heart_rate)

        print("\n--- User Information ---")
        print(f"Age: {age}")
        print(f"Weight: {weight} lbs")
        print(f"Height: {height} in")
        print(f"Diabetes Type: {diabetes_type}")

        print("\n--- Sensor Readings ---")
        print(f"Heart Rate: {heart_rate} bpm")
        print(f"Blood Oxygen: {blood_oxygen}%")

        print("\n--- Heart Rate Zones ---")
        print(f"Estimated Max Heart Rate: {max_hr:.0f} bpm")
        print(f"Moderate Exercise Zone: {mod_low:.1f} - {mod_high:.1f} bpm")
        print(f"Vigorous Exercise Zone: {mod_high:.1f} - {vig_high:.1f} bpm")
        print(f"Current Activity Level: {zone}")

    except Exception as e:
        print(f"Error reading sensor data: {e}")

    finally:
        ser.close()


if __name__ == "__main__":
    main()
