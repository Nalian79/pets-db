import csv
import logging
import psycopg2
import string
import sys

logging.basicConfig(filename="output.log", level=logging.DEBUG)

# Open and parse CSV file, create dict from what we find.

def readcsv(filename):
    """ Read in a CSV file and create a dict out of the data.
    Return this dict as a list for easy access later. Ensure that
    key values are lowercase. """
    logging.info("Reading in {!r}".format(filename))
    pet_info = []
    with open(filename, "r+") as f:
        logging.debug("Opened file {!r} successfully.".format(filename))
        reader = csv.DictReader(f, delimiter=',')
        # Strip whitespace from key/value pairs, lowercase keys
        reader = (dict(
                (k.strip().lower(), v.strip())
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

    # Insert data into db by looping through the list of pets and
    for pet in pet_list:
        pet_name = pet['name']
        logging.debug("Trying to insert {!r}, {!r}, {!r}".format(
                pet['name'], pet['adopted'], pet['age']))
        add_pet_query = "INSERT INTO pet (name, adopted, age) VALUES \
                       (%(name)s, %(adopted)s, %(age)s)"
        cur.execute(add_pet_query, pet)

        # If we encounter a shelter that isn't in our DB, add it.  If it is
        # present, insert the appropriate shelter_id into the pet row.
        shelter_name = pet['shelter name']
        if shelter_name !=None:
            logging.debug("Looking up or adding {!r}".format(shelter_name))
            is_sid_query = "insert into shelter (name) values ('%s') except \
                (select name from shelter where \
                name='%s')" % (shelter_name, shelter_name)
            cur.execute(is_sid_query, pet)
            add_sid_query = "update pet set shelter_id = shelter.id from \
                shelter where shelter.name='%s' and \
                pet.name='%s'" % (shelter_name, pet_name)
            cur.execute(add_sid_query, pet)

        # If we encounter a species that isn't in our DB, add it.  If it is
        # present, do nothing.
        species_name = pet['species name']
        if species_name !=None:
            # Capitalize the first letter for normalization.
            species_name = string.capwords(species_name)
            logging.debug("Looking up or adding {!r} to species table".format(
                    species_name))
            species_exist_query = "insert into species (name) values ('%s') \
                except (select name from species where \
                name='%s')" % (species_name, species_name)
            cur.execute(species_exist_query, pet)


        # If we encounter a breed that isn't in our DB, add it.  If it is
        # present, insert the appropriate breed_id into the pet row.
        breed_name = pet['breed name']
        if breed_name !=None:
            # Capitalize the first letter in the breed name to normalize
            breed_name = string.capwords(breed_name)
            logging.debug("Looking up or adding {!r} to the breed table".format(
                    breed_name))
            is_bid_query = "insert into breed (name) values \
                ('%s') except \
                (select name from breed where \
                name='%s')" % (breed_name, breed_name)
            cur.execute(is_bid_query, pet)
            # Too many issues with except clause to add species_id at the same
            # time, do that now.
            norm_breed_query = "update breed set species_id = species.id \
                from species where species.name='%s' and \
                breed.name='%s'" % (species_name, breed_name)
            cur.execute(norm_breed_query, pet)
            add_bid_query = "update pet set breed_id = breed.id from \
                breed where breed.name='%s' and \
                pet.name='%s'" % (breed_name, pet_name)
            cur.execute(add_bid_query, pet)


    conn.commit()
    cur.close()
    conn.close()


def dict_print(pet_list):
    """ Used for debugging purposes.  Print out the records in
    the dictionary so we can change up the key:value pairs as needed. """
    for pet in pet_list:
        print "Record Start"
        for key in pet:
            print key, ':', pet[key]

def main():
    """ Main function """
    logging.info("Starting script..")
    # Lets make sure we can read in the CSV file and get a valid dict.
    file_name="pets_to_add.csv"
    print "Starting script!  Let's import your data."

    # Create list of pets, put their info into a dictionary
    print "Importing data from", file_name
    pet_list = readcsv(file_name)

    # Add pets to the db
    print "Adding data to the database...",
    try:
        add_pets(pet_list)
    except MyException:
        print "Sorry, I was unable to import your data."
    else:
        print "Data imported!  Check out the DB."

if __name__ == "__main__":
    main()
