import random
import math

# Creates a csv file with random sky coordinates and search radius

# Set up sine distribution number generator
def sin_distribution_random():
    u = random.random()
    return math.acos(1 - 2 * u)

# Generate random numbers for dec (sine) and ra (uniform)
def generate_random_coordinates(num_coordinates):
    ra_rand_dist = [random.uniform(0, 360) for _ in range(num_coordinates)]
    dec_sin_dist = [(sin_distribution_random()*180/math.pi - 90) for _ in range(num_coordinates)]
    return [ra_rand_dist, dec_sin_dist]


def store_sky_coordinate_data(filename, num_coordinates, radius):
    # generate list of random sky coordinates following desired distribution
    [ra_rand_dist, dec_sin_dist] = generate_random_coordinates(num_coordinates)

    # write header
    with open(filename, "w") as file:
        file.write("Coordinate Number, RA_CTR, DEC_CTR, Radius \n")

        # loop through coordinates and write them to the file
        for i in range(len(ra_rand_dist)):
            ra = str(ra_rand_dist[i])
            dec = str(dec_sin_dist[i])
            file.write(f"{i}, {ra}, {dec}, {radius} \n")


# create csv file
if __name__ == "__main__": 
    filename = f"random_sky_coordinates.csv"
    num_coordinates = 1000
    radius = 100

    store_sky_coordinate_data(filename, num_coordinates, radius)