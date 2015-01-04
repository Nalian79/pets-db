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
        for row in reader:
            pet_info.append(row)
            logging.debug("Inserted {!r} into list".format(row))
    return pet_info

def add_pets(pet_list, database="pets"):
    """Add pets to our database from the csv file we parsed into a list """

    logging.debug("Trying database connection.")
    try:
        conn=psycopg2.connect(database=database)
    except:
        print "Couldn't connect to the DB!"

    cur=conn.cursor()

    for item in pet_list:
        logging.debug("Trying to insert {!r}".format(item))
        query = "INSERT INTO pet (name) VALUES ({!r})".format(
            item['Name'])
        cur.executemany(query, item)

    conn.commit()
    cur.close()
    conn.close()


def main():
    """ Main function """
    logging.info("Starting script..")
    # Lets make sure we can read in the CSV file and get a valid dict.
    file_name="pets_to_add.csv"
    # Create list of pet info in dict format
    pet_list = readcsv(file_name)

    # Add pets to the db
    add_pets(pet_list)



if __name__ == "__main__":
    main()
