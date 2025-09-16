# This script contains the function definition to compute the 
# Julia set function. 
def calculate_z_serial_purepython(maxiter, zs, cs):
    '''
    Calculate output list using Julia update rule
    '''
    output = [0] * len(zs) # list of zeros
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while abs(z) < 2 and n < maxiter:
            z = z * z + c
            n += 1
        output[i] = n
    return output