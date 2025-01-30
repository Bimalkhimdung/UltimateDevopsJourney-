def user_input():
    weight = float(input("Enter your weight: "))
    height = float(input("Enter your height: "))

    return(weight,height)
def calulate_bmi(weight,height):
    bmi = weight/(height*height)
    if bmi < 18.5:
        print(f"your are underweight:" , bmi)
    elif bmi <24.9:
        print("your are Normal Weight: ", bmi)
    elif bmi <= 25 and bmi < 29.9:
        print("You are overweight: ", bmi)
    else:
        print("Your are Obese: ", bmi)

weight, height = user_input()
calulate_bmi(weight,height)