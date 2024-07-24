def roundr(num, ndigit=1) -> float | str:
    """
# roundr
## Rounds a number to a specified number of decimal places.

param num : The number you want to round. It can be provided as a string or an integer/decimal.
param ndigit : The number of decimal places to which you want to round the number.\n
This function returns the rounded number as a float.

Example:
    >>> roundr(349.5)
    350
    
    >>> roundr(6.54,1) | roundr(6.54)
    6.5
    
    >>> roundr('6.55')
    6.6
    
    >>> roundr(6.56,'1')
    6.6
    
    >>> roundr(6,'e')
    "Invalid input, try again!"

    >>> roundr('r',3)
    "Invalid input, try again!"
    
    """
    
    try:
        num = float(num)   # Convert the input to a float
        ndigit = int(ndigit)  # Convert the number of decimal places to an integer
        
    except ValueError:
        print("Invalid input, try again!")  # Handle the case where conversion fails
        return

    num_str = str(num)  # Convert the number to a string
    
    # Find the position of the decimal point
    index_base = num_str.index('.')
    index_tar = index_base + ndigit + 1  # Position of the digit to decide rounding

    # Extract the digit after the rounding position to decide rounding
    if index_tar < len(num_str):
        real_index_tar = int(num_str[index_tar])
    else:
        real_index_tar = 0  # Default to 0 if there are not enough digits
    
    if real_index_tar >= 5:
        # Perform rounding up
        num_list = list(num_str)        
        carry_index = index_tar - 1  # Position to check for carry-over
        
        while carry_index >= 0:
            if num_list[carry_index] == '.':
                carry_index -= 1
                continue
            
            if num_list[carry_index] == '9':
                num_list[carry_index] = '0'  # Carry over if the digit is 9
                
            else: # Digits 0-8
                num_list[carry_index] = str(int(num_list[carry_index]) + 1)  # Increment the digit
                break
            
            carry_index -= 1
            
        # Check if all digits have turned to '0' and handle the case by adding '1' to the start
        if carry_index < 0:  # Example: ["0","0","0",...] means rounding 999 to 1000
            num_list.insert(0, '1')
        
        rounded_num = ''.join(num_list[:index_tar])  # Combine the list back to a string
    else:
        rounded_num = num_str[:index_tar]  # If no rounding up is needed, just truncate
    
    round_num = float(rounded_num)  # Convert the rounded number back to float
    print(round_num)  # Output the rounded number
    return round_num
