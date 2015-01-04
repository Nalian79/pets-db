import csv
import logging
import psycopg2
import sys

logging.basicConfig(filename="output.log", level=logging.DEBUG)

# Open and parse CSV file, create dict from what we find.

def readcsv(filename):
    """ Read in a CSV file and create a dict out of the data.
    Return this dict as a list for easy access later. Ensure that
    values are lowercase. """
    logging.info("Reading in {!r}".format(filename))
    pet_info = []
    with open(filename, "r+") as f:
        logging.debug("Opened file {!r} successfully.".format(filename))
        reader = csv.DictReader(f, delimiter=',')
        # Strip whitespace from key/value pairs
        reader = (dict(
                (k.strip(), v.strip())
                for k, v in row.items()) for row in reader)
        for row in reader:
            pet_info.append(row)
            logging.debug("Inserted {!r} into list".format(row))
        for pet in pet_info:
            for key in pet:
                if pet[key] == '':
                    pet[key] = None
    return pet_info


def add_pets(pet_list, database="pets"):
    """Add pets to our database from the csv file we parsed into a list """

    logging.debug("Trying database connection.")
    try:
        conn=psycopg2.connect(database=database)
    except:
        print "Couldn't connect to the DB!"

    cur=conn.cursor()
    # Insert initial data into the pet table
    for pet in pet_list:
        logging.debug("Trying to insert {!r}".format(pet))
        query = "INSERT INTO pet (name, adopted, age) \
                VALUES (%(Name)s, %(adopted)s, %(age)s)"
        cur.execute(query, pet)
    conn.commit()
    cur.close()
    conn.close()

def dict_work(pet_list):

    for pet in pet_list:
        print "Record Start"
        for key in pet:
            print key, pet[key]

def main():
    """ Main function """
    logging.info("Starting script..")
    # Lets make sure we can read in the CSV file and get a valid dict.
    file_name="pets_to_add.csv"
    # Create list of pets, put their info into a dictionary
    pet_list = readcsv(file_name)

    # Add pets to the db
    add_pets(pet_list)
#    dict_work(pet_list)


if __name__ == "__main__":
    main()
