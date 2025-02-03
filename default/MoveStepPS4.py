from ps4 import *
print("Helllldlsfjlmf")
while True:
    print("Hello")

    PS4State = Return()
    os.system('clear')
    print(f"XButton: {PS4State[0]}, TButton: {PS4State[1]}, CButton: {PS4State[2]}, SButton: {PS4State[3]}")
    print(f"L1Button: {PS4State[4]}, L2Button: {PS4State[5]}, R1Button: {PS4State[6]}, R2Button: {PS4State[7]}")
    print(f"UpArrow: {PS4State[8]}, DownArrow: {PS4State[9]}, LeftArrow: {PS4State[10]}, RightArrow: {PS4State[11]}")
    print(f"L3Button: {PS4State[12]}, R3Button: {PS4State[13]}, OptionsButton: {PS4State[14]}, ShareButton: {PS4State[15]}, PSButton: {PS4State[16]}")
    print(f"L3X: {round(PS4State[17],2)}, L3Y: {round(PS4State[18],2)}")
    print(f"R3X: {round(PS4State[19],2)}, R3Y: {round(PS4State[20],2)}")
    
    time.sleep(0.02)
