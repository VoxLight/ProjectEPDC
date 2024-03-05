
import database
import utils
import random



def main():

    # Set up the logger and config
    log = utils.get_logger()
    config = utils.Config()
    log.info('Starting....')

    # Add a user to the database
    db = database.connection.Database(config)
    
    user = database.models.Member(name='John Doe', discord_id=str(random.randint(100000000, 999999999)))
    db.session.add(user)
    db.session.commit()
    db.session.close()
    log.info('User added to the database.')

    # Try to pull the info from the database
    membrs = db.session.query(database.models.Member).all()
    for membr in membrs:
        log.info(f'User: {membr.name}')
    
    db.session.close()


if __name__ == "__main__":
    main()