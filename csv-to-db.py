import csv
import logging
#import psycopg2
import sys

logging.basicConfig(filename="output.log", level=logging.DEBUG)

# Open and parse CSV file, create dict from what we find.

def readcsv(filename):
    """ Read in a CSV file and create a dict out of the data """
    logging.info("Reading in {!r}".format(filename))
    with open(filename, "r+") as f:
        logging.debug("Opened file {!r} successfully.".format(filename))
        reader = csv.DictReader(f, delimiter=',')
        pet_info = []
        for row in reader:
            pet_info.append(row)
            logging.debug("Inserted contents into dict: {!r}".format(row))
        return pet_info

def main():
    """ Main function
    Changing purpose as the script grows...
    """
    logging.info("Starting script..")
    # Lets make sure we can read in the CSV file and get a valid dict.
    file_name="pets_to_add.csv"
    pet_list = readcsv(file_name)
    logging.info("Trying to read in {!r}.".format(file_name))
    for item in pet_list:
        print item


if __name__ == "__main__":
    main()
