import serial
import time


def get_user_inputs():
    age = int(input("Enter your age: "))
    weight = float(input("Enter your weight (in pounds): "))
    height = float(input("Enter your height (in inches): "))
    diabetes_type = input("Do you have Type 1, Type 2, or no diabetes? (T1/T2/NONE): ").strip().upper()

    return age, weight, height, diabetes_type


#def connect_to_arduino(port='COM3', baud_rate=9600):
    """
    Opens serial connection to Arduino.
    Change COM3 to the correct port on your computer.
    """
   # ser = serial.Serial(port, baud_rate, timeout=2)
    #time.sleep(2)
    #return ser


#def get_sensor_data(ser):
    """
    Expected Arduino data format:
    heart_rate,blood_oxygen,bgl
    Example:
    85,98,110
    """
 #   line = ser.readline().decode('utf-8').strip()

  #  if not line:
   #     raise ValueError("No data received from Arduino.")

    #parts = line.split(',')

    #if len(parts) != 3:
     #   raise ValueError(f"Unexpected data format: {line}")

    #heart_rate = int(parts[0])
    #blood_oxygen = float(parts[1])
   # bgl = int(parts[2])

  #  return heart_rate, blood_oxygen, bgl


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
        zone = "RHR"

    return max_heart_rate, moderate_low, moderate_high, vigorous_high, zone


def get_spo2_zone(spo2_data):
    if 92 < spo2_data <= 97.5:
        spo2_zone = "high"
    elif 97.5 < spo2_data <= 98.5:
        spo2_zone = "Rest"
    elif 98.5 < spo2_data <= 100:
        spo2_zone = "anaero"
    else:
        spo2_zone = "unknown"

    return spo2_zone


def bgl_thresh_zones(hr_zone, spo2_zone):
    if hr_zone == "Vigorous Exercise" and spo2_zone == "high":
        top_thresh = 126
        bottom_thresh = 90
    elif hr_zone == "Vigorous Exercise" and spo2_zone == "Rest":
        top_thresh = 180
        bottom_thresh = 126
    elif hr_zone == "Vigorous Exercise" and spo2_zone == "anaero":
        top_thresh = 126
        bottom_thresh = 90
    elif hr_zone == "Moderate Exercise" and spo2_zone == "high":
        top_thresh = 126
        bottom_thresh = 90
    elif hr_zone == "Moderate Exercise" and spo2_zone == "Rest":
        top_thresh = 180
        bottom_thresh = 126
    elif hr_zone == "Moderate Exercise" and spo2_zone == "anaero":
        top_thresh = 180
        bottom_thresh = 126
    elif hr_zone == "RHR" and spo2_zone == "high":
        top_thresh = 200
        bottom_thresh = 80
    elif hr_zone == "RHR" and spo2_zone == "Rest":
        top_thresh = 200
        bottom_thresh = 80
    else:
        top_thresh = 200
        bottom_thresh = 80

    return top_thresh, bottom_thresh


def get_bgl_warning(bgl_data, top_thresh, bottom_thresh):
    if bgl_data >= top_thresh:
        return "Hyper Attack!"
    elif bgl_data <= bottom_thresh:
        return "Hypo Attack!"
    else:
        return "You're not dying! Yippeeeeee!"


def main():
    age, weight, height, diabetes_type = get_user_inputs()

    print("\nConnecting to Arduino...")
    ser = connect_to_arduino()

    try:
        heart_rate = 
        blood_oxygen =  
        bgl_data = 

        max_hr, mod_low, mod_high, vig_high, hr_zone = get_heart_rate_zone(age, heart_rate)
        spo2_zone = get_spo2_zone(blood_oxygen)
        top_thresh, bottom_thresh = bgl_thresh_zones(hr_zone, spo2_zone)
        warning = get_bgl_warning(bgl_data, top_thresh, bottom_thresh)

        print("\n--- User Information ---")
        print(f"Age: {age}")
        print(f"Weight: {weight} lbs")
        print(f"Height: {height} in")
        print(f"Diabetes Type: {diabetes_type}")

        print("\n--- Sensor Readings ---")
        print(f"Heart Rate: {heart_rate} bpm")
        print(f"Blood Oxygen: {blood_oxygen}%")
        print(f"Blood Glucose Level: {bgl_data} mg/dL")

        print("\n--- Heart Rate Zone Info ---")
        print(f"Estimated Max Heart Rate: {max_hr:.1f} bpm")
        print(f"Moderate Zone: {mod_low:.1f} - {mod_high:.1f} bpm")
        print(f"Vigorous Zone: {mod_high:.1f} - {vig_high:.1f} bpm")
        print(f"Current Heart Rate Zone: {hr_zone}")

        print("\n--- Blood Oxygen Zone Info ---")
        print(f"Current SpO2 Zone: {spo2_zone}")

        print("\n--- BGL Thresholds for These Zones ---")
        print(f"Low Threshold: {bottom_thresh} mg/dL")
        print(f"High Threshold: {top_thresh} mg/dL")

        print("\n--- Warning Status ---")
        print(warning)

    except ValueError as e:
        print(f"Error: {e}")

    finally:
        ser.close()


if __name__ == "__main__":
    main()
