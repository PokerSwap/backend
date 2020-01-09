# from flask_sqlalchemy import SQLAlchemy
from models import db, Users, Profiles, Tournaments, Swaps, Flights, Buy_ins, Transactions, Devices
from datetime import datetime, timedelta
from utils import sha256

# db = SQLAlchemy('postgres://Francine@localhost/swapprofit')

def run_seeds():


    Devices.query.delete()
    Transactions.query.delete()
    Buy_ins.query.delete()
    Swaps.query.delete()
    Flights.query.delete()
    Tournaments.query.delete()
    Profiles.query.delete()
    Users.query.delete()

    db.session.execute("ALTER SEQUENCE users_id_seq RESTART")
    db.session.execute("ALTER SEQUENCE tournaments_id_seq RESTART")
    db.session.execute("ALTER SEQUENCE flights_id_seq RESTART")
    db.session.execute("ALTER SEQUENCE buy_ins_id_seq RESTART")
    db.session.execute("ALTER SEQUENCE swaps_id_seq RESTART")
    db.session.execute("ALTER SEQUENCE transactions_id_seq RESTART")
    db.session.execute("ALTER SEQUENCE devices_id_seq RESTART")

    ########################
    #  USERS AND PROFILES
    ########################

    lou = Users(
        email='lou@gmail.com',
        password=sha256('loustadler'),
        status='valid'
    )
    db.session.add(lou)
    lou = Profiles(
        first_name='Luiz', 
        last_name='Stadler',
        nickname='Lou',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=207424',
        profile_pic_url='https://pokerdb.thehendonmob.com/pictures/Lou_Stadler_Winner.JPG',
        user=lou
    )
    db.session.add(lou)

    cary = Users(
        email='katz234@gmail.com',
        password=sha256('carykatz'),
        status='valid'
    )
    db.session.add(cary)
    cary = Profiles(
        first_name='Cary', 
        last_name='Katz',
        nickname='',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=26721',
        profile_pic_url='https://pokerdb.thehendonmob.com/pictures/carykatzpic.png',
        user=cary
    )
    db.session.add(cary)

    kate = Users(
        email='hoang28974@gmail.com',
        password=sha256('kateHoang'),
        status='valid'
    )
    db.session.add(kate)
    kate = Profiles(
        first_name='Kate', 
        last_name='Hoang',
        nickname='',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=421758',
        profile_pic_url='https://pokerdb.thehendonmob.com/pictures/Hoang_2.jpg',
        user=kate
    )
    db.session.add(kate)

    nikita = Users(
        email='mikitapoker@gmail.com',
        password=sha256('nikitapoker'),
        status='valid'
    )
    db.session.add(nikita)
    nikita = Profiles(
        first_name='Nikita', 
        last_name='Bodyakovskiy',
        nickname='Mikita',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=159100',
        profile_pic_url='https://pokerdb.thehendonmob.com/pictures/NikitaBadz18FRh.jpg',
        user=nikita
    )
    db.session.add(nikita)

    ########################
    #     TOURNAMENTS
    ########################

    heartland = Tournaments(
        name='Heartland Poker Tour - HPT Colorado, Black Hawk',
        address='261 Main St',
        city='Black Hawk',
        state='CO',
        zip_code='80422',
        latitude=39.801105,
        longitude=-105.503991,
        start_at=datetime(2019,10,11,12)
    )
    db.session.add(heartland)

    stones = Tournaments(
        name='Stones Live Fall Poker Series',
        address='6510 Antelope Rd',
        city='Citrus Heights',
        state='CA',
        zip_code='95621',
        latitude=38.695155,
        longitude=-121.307501,
        start_at=datetime(2019,9,30,11)
    )
    db.session.add(stones)

    wpt = Tournaments(
        name='WPT DeepStacks - WPTDS Sacramento',
        address='Thunder Valley Casino Resort, 1200 Athens Ave',
        city='Lincoln',
        state='CA',
        zip_code='95648',
        latitude=38.904035,
        longitude=-121.295541,
        start_at=datetime(2019,10,2,12)
    )
    db.session.add(wpt)

    now = datetime.utcnow()
    live = Tournaments(
        name='WPT DeepStacks - LIVE',
        address='Thunder Valley Casino Resort, 1200 Athens Ave',
        city='Lincoln',
        state='CA',
        zip_code='95648',
        latitude=38.904035,
        longitude=-121.295541,
        start_at=now - timedelta(days=2)
    )
    db.session.add(live)

    ########################
    #       FLIGHTS
    ########################

    flight1_live = Flights(
        start_at=now,
        end_at=now + timedelta(hours=5),
        tournament=live,
        day=1
    )
    flight2_live = Flights(
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=5),
        tournament=live,
        day=2
    )
    db.session.add_all([flight1_live, flight2_live])


    flight1_heartland = Flights(
        start_at=datetime(2019,10,11,12),
        end_at=datetime(2019,10,11,16),
        tournament=heartland,
        day=1
    )
    flight2_heartland = Flights(
        start_at=datetime(2019,10,11,16),
        end_at=datetime(2019,10,11,21),
        tournament=heartland,
        day=1
    )
    db.session.add_all([flight1_heartland, flight2_heartland])


    flight1_stones = Flights(
        start_at=datetime(2019,9,30,12),
        end_at=datetime(2019,9,30,15),
        tournament=stones,
        day=1
    )
    flight2_stones = Flights(
        start_at=datetime(2019,9,30,15),
        end_at=datetime(2019,9,30,21),
        tournament=stones,
        day=1
    )
    flight3_stones = Flights(
        start_at=datetime(2019,10,1,12),
        end_at=datetime(2019,10,1,21),
        tournament=stones,
        day=2
    )
    db.session.add_all([flight1_stones, flight2_stones, flight3_stones])


    flight1_wpt = Flights(
        start_at=datetime(2019,10,2,12),
        end_at=datetime(2019,10,2,22),
        tournament=wpt,
        day=1
    )
    db.session.add(flight1_wpt)


    ########################
    #        SWAPS
    ########################

    s1 = Swaps(
        tournament=heartland,
        sender_user=lou,
        recipient_user=cary,
        percentage=10,
        status='pending',
        due_at=(heartland.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=heartland,
        sender_user=cary,
        recipient_user=lou,
        percentage=10,
        status='incoming',
        due_at=(heartland.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    

    s1 = Swaps(
        tournament=heartland,
        sender_user=nikita,
        recipient_user=kate,
        percentage=15,
        status='pending',
        due_at=(heartland.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=heartland,
        sender_user=kate,
        recipient_user=nikita,
        percentage=15,
        status='incoming',
        due_at=(heartland.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=heartland,
        sender_user=lou,
        recipient_user=kate,
        percentage=5,
        status='incoming',
        due_at=(heartland.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=heartland,
        sender_user=kate,
        recipient_user=lou,
        percentage=5,
        status='pending',
        due_at=(heartland.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=cary,
        percentage=10,
        status='pending',
        due_at=(live.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=live,
        sender_user=cary,
        recipient_user=lou,
        percentage=9,
        status='incoming',
        due_at=(live.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=live,
        sender_user=nikita,
        recipient_user=kate,
        percentage=15,
        status='pending',
        due_at=(live.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=live,
        sender_user=kate,
        recipient_user=nikita,
        percentage=15,
        status='incoming',
        due_at=(live.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=kate,
        percentage=5,
        status='incoming',
        due_at=(live.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=live,
        sender_user=kate,
        recipient_user=lou,
        percentage=5,
        status='pending',
        due_at=(live.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=wpt,
        sender_user=lou,
        recipient_user=cary,
        percentage=10,
        status='pending',
        due_at=(wpt.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=wpt,
        sender_user=cary,
        recipient_user=lou,
        percentage=10,
        status='incoming',
        due_at=(wpt.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=wpt,
        sender_user=nikita,
        recipient_user=kate,
        percentage=15,
        status='pending',
        due_at=(wpt.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=wpt,
        sender_user=kate,
        recipient_user=nikita,
        percentage=15,
        status='incoming',
        due_at=(wpt.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=wpt,
        sender_user=cary,
        recipient_user=kate,
        percentage=5,
        status='pending',
        due_at=(wpt.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=wpt,
        sender_user=kate,
        recipient_user=cary,
        percentage=5,
        status='incoming',
        due_at=(wpt.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    ########################
    #       BUY INS
    ########################

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=2,
        user=lou,
        flight=flight1_live
    ))

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=4,
        user=lou,
        flight=flight1_live
    ))

    db.session.add(Buy_ins(
        chips=500,
        table=7,
        seat=1,
        user=cary,
        flight=flight1_live
    ))

    db.session.add(Buy_ins(
        chips=500,
        table=3,
        seat=2,
        user=cary,
        flight=flight2_live
    ))

    db.session.add(Buy_ins(
        chips=1000,
        table=2,
        seat=2,
        user=kate,
        flight=flight2_live
    ))

    db.session.add(Buy_ins(
        chips=300,
        table=2,
        seat=2,
        user=kate,
        flight=flight2_live
    ))
    
    db.session.add(Buy_ins(
        chips=700,
        table=3,
        seat=1,
        user=nikita,
        flight=flight2_live
    ))

    ######################
    #   INCOMING SWAPS
    ######################

    s1 = Swaps(
        tournament=live,
        sender_user=kate,
        recipient_user=cary,
        percentage=10,
        due_at=(live.start_at + timedelta(days=4)),
        status='incoming'
    )
    s2 = Swaps(
        tournament=live,
        sender_user=cary,
        recipient_user=kate,
        percentage=5,
        due_at=(live.start_at + timedelta(days=4)),
        status='pending',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    ####################################
    #   UPCOMING TOURNAMENT + FLIGHTS
    ####################################

    newvegas = Tournaments(
        name='New Vegas Strip - Texas Hold\'em Finale',
        address='129 East Fremont St.',
        city='Las Vegas',
        state='NV',
        zip_code='89101',
        latitude=36.172082,
        longitude=-115.122366,
        start_at=datetime(2281,10,11,10)
    )
    flight1_newvegas = Flights(
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=5),
        tournament=newvegas,
        day=1
    )
    flight2_newvegas = Flights(
        start_at=now + timedelta(days=1, hours=6),
        end_at=now + timedelta(days=1, hours=12),
        tournament=newvegas,
        day=1
    )
    db.session.add_all([newvegas, flight1_newvegas, flight2_newvegas])


    #######################
    #   UPCOMING BUYINS
    #######################
    
    db.session.add(Buy_ins(         
        chips=5000,         
        table=4,         
        seat=2,         
        user=lou,        
        flight=flight1_newvegas     
    ))
    db.session.add(Buy_ins(         
        chips=4000,         
        table=1,         
        seat=12,         
        user=cary,        
        flight=flight1_newvegas     
    ))
    db.session.add(Buy_ins(         
        chips=9000,         
        table=22,         
        seat=7,         
        user=lou,        
        flight=flight2_newvegas     
    ))
    db.session.add(Buy_ins(         
        chips=6000,         
        table=5,         
        seat=4,         
        user=nikita,        
        flight=flight2_newvegas     
    ))

    #####################
    #   AGREED SWAPS
    #####################

    s1 = Swaps(
        tournament=newvegas,
        sender_user=lou,
        recipient_user=cary,
        percentage=8,
        due_at=(newvegas.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament= newvegas,
        sender_user=cary,
        recipient_user=lou,
        percentage=2,
        due_at=(newvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    ######################
    #   REJECTED SWAPS
    ######################

    s1 = Swaps(
        tournament=newvegas,
        sender_user=lou,
        recipient_user=nikita,
        percentage=40,
        due_at=(newvegas.start_at + timedelta(days=4)),
        status='rejected'
    )
    s2 = Swaps(
        tournament= newvegas,
        sender_user=nikita,
        recipient_user=lou,
        percentage=40,
        due_at=(newvegas.start_at + timedelta(days=4)),
        status='rejected',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    #####################
    #   CANCELED SWAPS
    #####################

    s1 = Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=nikita,
        percentage=20,
        due_at=(live.start_at + timedelta(days=4)),
	    status='canceled'
    )
    s2 = Swaps(
        tournament= live,
        sender_user=nikita,
        recipient_user=lou,
        percentage=20,
        due_at=(live.start_at + timedelta(days=4)),
	    status='canceled',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    ######################
    #   PAST TOURNAMENT
    ######################

    oldvegas = Tournaments(
        name='Old Vegas Strip - Poker Eyes \'90',
        address='2211 N Rampart Blvd',
        city='Las Vegas',
        state='NV',
        zip_code='89145',
        latitude=36.1683,
        longitude=-115.2660,
        start_at=datetime(1990,5,2,10)
    )
    flight1_oldvegas = Flights(
        start_at=datetime(1990,5,2,10),
        end_at=now + timedelta(days=1, hours=5),
        tournament=oldvegas,
        day=1
    )
    db.session.add_all([oldvegas, flight1_oldvegas])


    db.session.add(Buy_ins(         
        chips=7500,         
        table=14,         
        seat=12,         
        user=lou,        
        flight=flight1_oldvegas     
    ))
    db.session.add(Buy_ins(         
        chips=4500,         
        table=21,         
        seat=1,         
        user=cary,        
        flight=flight1_oldvegas     
    ))
    db.session.add(Buy_ins(         
        chips=5500,         
        table=1,         
        seat=7,         
        user=nikita,        
        flight=flight1_oldvegas     
    ))
    db.session.add(Buy_ins(         
        chips=9000,         
        table=13,         
        seat=12,         
        user=kate,        
        flight=flight1_oldvegas     
    ))


    s1 = Swaps(
        tournament=oldvegas,
        sender_user=lou,
        recipient_user=cary,
        percentage=5,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=cary,
        recipient_user=lou,
        percentage=7,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=oldvegas,
        sender_user=lou,
        recipient_user=nikita,
        percentage=5,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        paid=True
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=nikita,
        recipient_user=lou,
        percentage=7,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=oldvegas,
        sender_user=lou,
        recipient_user=kate,
        percentage=15,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='pending'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=kate,
        recipient_user=lou,
        percentage=17,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='incoming',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    ##################
    # NEW TOURNAMENT
    ##################

    gamorrah = Tournaments(
        name='Final Days Poker at Gamorrah Casino',
        address='200 Fremont St',
        city='Las Vegas',
        state='NV',
        zip_code='89101',
        latitude=36.4683,
        longitude=-115.4660,
        start_at=datetime(2281,10,11,12)
    )
    flight1_gamorrah = Flights(
        start_at=datetime(2281,10,11,12),
        end_at=datetime(2281,10,11,16),
        tournament=gamorrah,
        day=1
    )
    flight2_gamorrah = Flights(
        start_at=datetime(2281,10,11,16),
        end_at=datetime(2281,10,11,21),
        tournament=gamorrah,
        day=1
    )
    db.session.add_all([gamorrah, flight1_gamorrah, flight2_gamorrah])


    db.session.add(Buy_ins(
        chips=13000,
        table=13,
        seat=3,
        user=kate,
        flight=flight1_gamorrah
    ))

    # TOURNAMENTS
    p2 = Tournaments(
        name='Placeholder Tournament 1',
        address='2211 N Rampart Blvd',
        city='Charlotte',
        state='NC',
        zip_code='28105',
        latitude=35.2271,
        longitude=-80.8431,
        start_at=datetime(1994,5,2,10)
    )
    f1_p2 = Flights(
        start_at=datetime(1994,5,2,10),
        tournament=p2
    )
    db.session.add_all([p2, f1_p2])

    p2 = Tournaments(
        name='Placeholder Tournament 2',
        address='2211 N Rampart Blvd',
        city='Albany',
        state='NY',
        zip_code='12084',
        latitude=42.6526,
        longitude=-73.7562,
        start_at=datetime(1998,5,2,10)
    )
    f1_p2 = Flights(
        start_at=datetime(1998,5,2,10),
        tournament=p2
    )
    db.session.add_all([p2, f1_p2])

    p2 = Tournaments(
        name='Placeholder Tournament 3',
        address='2211 N Rampart Blvd',
        city='New Orleans',
        state='LA',
        zip_code='70032',
        latitude=29.9511,
        longitude=-90.0715,
        start_at=datetime(2002,5,2,10)
    )
    f1_p2 = Flights(
        start_at=datetime(2002,5,2,10),
        tournament=p2
    )
    db.session.add_all([p2, f1_p2])

    p2 = Tournaments(
        name='Placeholder Tournament 4',
        address='2211 N Rampart Blvd',
        city='West Palm Beach',
        state='FL',
        zip_code='33401',
        latitude=26.7153,
        longitude=-80.0534,
        start_at=datetime(2019,5,2,10)
    )
    f1_p2 = Flights(
        start_at=datetime(2019,5,2,10),
        tournament=p2
    )
    db.session.add_all([p2, f1_p2])

    p2 = Tournaments(
        name='Placeholder Tournament 5',
        address='2211 N Rampart Blvd',
        city='Jacksonville',
        state='FL',
        zip_code='32034',
        latitude=30.3322,
        longitude=-81.6557,
        start_at=datetime(2019,5,3,10)
    )
    f1_p2 = Flights(
        start_at=datetime(2019,5,3,10),
        tournament=p2
    )
    db.session.add_all([p2, f1_p2])

    p2 = Tournaments(
        name='Placeholder Tournament 6',
        address='2211 N Rampart Blvd',
        city='Atlanta',
        state='GA',
        zip_code='30301',
        latitude=33.7490,
        longitude=-84.3880,
        start_at=datetime(2019,5,4,10)
    )
    f1_p2 = Flights(
        start_at=datetime(2019,5,4,10),
        tournament=p2
    )
    db.session.add_all([p2, f1_p2])

    p2 = Tournaments(
        name='Placeholder Tournament 7',
        address='2211 N Rampart Blvd',
        city='Los Angeles',
        state='CA',
        zip_code='90001',
        latitude=33.7866,
        longitude=-118.2987,
        start_at=datetime(2019,5,5,10)
    )
    f1_p2 = Flights(
        start_at=datetime(2019,5,5,10),
        tournament=p2
    )
    db.session.add_all([p2, f1_p2])

    p2 = Tournaments(
        name='Placeholder Tournament 8',
        address='2211 N Rampart Blvd',
        city='Seattle',
        state='WA',
        zip_code='98101',
        latitude=47.6488,
        longitude=-122.3964,
        start_at=datetime(2019,5,6,10)
    )
    f1_p2 = Flights(
        start_at=datetime(2019,5,6,10),
        tournament=p2
    )
    db.session.add_all([p2, f1_p2])

    p2 = Tournaments(
        name='Placeholder Tournament 9',
        address='2211 N Rampart Blvd',
        city='Dallas',
        state='TX',
        zip_code='75001',
        latitude=32.7767,
        longitude=-96.7970,
        start_at=datetime(2019,5,7,10)
    )
    f1_p2 = Flights(
        start_at=datetime(2019,5,7,10),
        tournament=p2
    )
    db.session.add_all([p2, f1_p2])

    p2 = Tournaments(
        name='Placeholder Tournament 10',
        address='2211 N Rampart Blvd',
        city='Bangor',
        state='ME',
        zip_code='04401',
        latitude=44.8016,
        longitude=-68.7712,
        start_at=datetime(2019,5,8,10)
    )
    f1_p2 = Flights(
        start_at=datetime(2019,5,8,10),
        tournament=p2
    )
    db.session.add_all([p2, f1_p2])


    # ONE
    ocean = Tournaments(
        name='Ocean’s Masters 11',
        address='3600 S Las Vegas Blvd',
        city='Las Vegas',
        state='NV',
        zip_code='89109',
        latitude=36.1126,
        longitude=-115.1767,
        start_at=datetime(2019,12,26,10)
    )
    flight1_ocean = Flights(
        start_at=datetime(2019,12,26,10),
        tournament= ocean
    )
    db.session.add_all([ocean, flight1_ocean])

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=2,
        user=cary,
        flight=flight1_ocean
    ))


    # TWO
    royale = Tournaments(
        name='Casino Royale 2020',
        address='One MGM Way',
        city='Springfield',
        state='MA',
        zip_code='01103',
        latitude=42.0988,
        longitude=-72.5877,
        start_at=datetime(2020,12,27,10)
    )
    flight1_royale = Flights(
        start_at=datetime(2020,12,27,10),
        tournament= royale
    )
    db.session.add_all([royale, flight1_royale])

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=2,
        user=cary,
        flight=flight1_royale
    ))


    # THREE
    loathing = Tournaments(
        name='Fear and Loathing in Final Bet',
        address='3799 S. Las Vegas Blvd',
        city='Las Vegas',
        state='NV',
        zip_code='89109',
        latitude=36.1026,
        longitude=-115.1703,
        start_at=datetime(2020,12,28,10)
    )
    flight1_loathing = Flights(
        start_at=datetime(2020,12,28,10),
        tournament= loathing
    )
    db.session.add_all([loathing, flight1_loathing])

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=2,
        user=cary,
        flight=flight1_loathing
    ))


    # FOUR
    country = Tournaments(
        name='No Country for Dead Hands',
        address='287 Carrizo Canyon Rd',
        city='Mescalero',
        state='NM',
        zip_code='12084',
        latitude=33.2956,
        longitude=-105.6901,
        start_at=datetime(2020,12,29,10)
    )
    flight1_country = Flights(
        start_at=datetime(2020,12,29,10),
        tournament= country
    )
    db.session.add_all([country, flight1_country])

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=2,
        user=cary,
        flight=flight1_country
    ))


    # FIVE
    hangover = Tournaments(
        name='The Hangover Part 2020',
        address='3570 S Las Vegas Blvd',
        city='Las Vegas',
        state='NV',
        zip_code='89109',
        latitude=36.1162,
        longitude=-115.1745,
        start_at=datetime(2020,12,30,10)
    )
    flight1_hangover = Flights(
        start_at=datetime(2020,12,30,10),
        tournament= hangover
    )
    db.session.add_all([hangover, flight1_hangover])

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=2,
        user=cary,
        flight=flight1_hangover
    ))


    # SIX
    king = Tournaments(
        name='King of Games 2020',
        address='1 Seminole Way',
        city='Hollywood',
        state='FL',
        zip_code='3314',
        latitude=26.0510,
        longitude=-80.2110,
        start_at=datetime(2020,12,31,10)
    )
    flight1_king = Flights(
        start_at=datetime(2020,12,31,10),
        tournament= king
    )
    db.session.add_all([king, flight1_king])

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=2,
        user=cary,
        flight=flight1_king
    ))


    # SEVEN
    kakegurui = Tournaments(
        name='Kakegurui All-In Stakes 2020',
        address='794 Lucky Eagle Dr',
        city='Eagle Pass',
        state='TX',
        zip_code='78852',
        latitude=28.6107,
        longitude=-100.4416,
        start_at=datetime(2021,1,1,10)
    )
    flight1_kakegurui = Flights(
        start_at=datetime(2021,1,1,10),
        tournament= kakegurui
    )
    db.session.add_all([kakegurui, flight1_kakegurui])

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=2,
        user=cary,
        flight=flight1_kakegurui
    ))


    # EIGHT
    ultimate = Tournaments(
        name='Ultimate Survivor 2020',
        address='2705 Central Ave',
        city='Hot Springs',
        state='AR',
        zip_code='71901',
        latitude=34.4840,
        longitude=-93.0592,
        start_at=datetime(2021,1,2,10)
    )
    flight1_ultimate = Flights(
        start_at=datetime(2021,1,2,10),
        tournament= ultimate
    )
    db.session.add_all([ultimate, flight1_ultimate])

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=2,
        user=cary,
        flight=flight1_ultimate
    ))


    # NINE
    thankyou = Tournaments(
        name='Thank You For Gambling ‘20',
        address='7002 Arundel Mills Cir #7777',
        city='Hanover',
        state='MD',
        zip_code='21076',
        latitude=39.1573,
        longitude=-76.7272,
        start_at=datetime(2021,1,3,10)
    )
    flight1_thankyou = Flights(
        start_at=datetime(2021,1,3,10),
        tournament= thankyou
    )
    db.session.add_all([thankyou, flight1_thankyou])

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=2,
        user=cary,
        flight=flight1_thankyou
    ))


    # TEN
    battle = Tournaments(
        name='Poker Battle Royale 2020',
        address='91 WA-108',
        city='Shelton',
        state='WA',
        zip_code='98584',
        latitude=47.1282,
        longitude=-123.1013,
        start_at=datetime(2021,1,4,10)
    )
    flight1_battle = Flights(
        start_at=datetime(2021,1,4,10),
        tournament= battle
    )
    db.session.add_all([battle, flight1_battle])

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=2,
        user=cary,
        flight=flight1_battle
    ))


    donkey21 = Tournaments(
        name="Donkey's Annual '21",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2021,3,9,10)
    )
    flight1_donkey21 = Flights(
        start_at=datetime(2021,3,9,10),
        tournament= donkey21,
        day=1
    )
    db.session.add_all([donkey21, flight1_donkey21])

    donkey22 = Tournaments(
        name="Donkey's Annual '22",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2022,3,9,10)
    )
    flight1_donkey22 = Flights(
        start_at=datetime(2022,3,9,10),
        tournament= donkey22,
        day=1
    )
    db.session.add_all([donkey22, flight1_donkey22])

    donkey23 = Tournaments(
        name="Donkey's Annual '23",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2023,3,9,10)
    )
    flight1_donkey23 = Flights(
        start_at=datetime(2023,3,9,10),
        tournament= donkey23,
        day=1
    )
    db.session.add_all([donkey23, flight1_donkey23])

    donkey24 = Tournaments(
        name="Donkey's Annual '24",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2024,3,9,10)
    )
    flight1_donkey24 = Flights(
        start_at=datetime(2024,3,9,10),
        tournament= donkey24,
        day=1
    )
    db.session.add_all([donkey24, flight1_donkey24])

    donkey25 = Tournaments(
        name="Donkey's Annual '25",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2025,3,9,10)
    )
    flight1_donkey25 = Flights(
        start_at=datetime(2025,3,9,10),
        tournament= donkey25,
        day=1
    )
    db.session.add_all([donkey25, flight1_donkey25])

    donkey26 = Tournaments(
        name="Donkey's Annual '26",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2026,3,9,10)
    )
    flight1_donkey26 = Flights(
        start_at=datetime(2026,3,9,10),
        tournament= donkey26,
        day=1
    )
    db.session.add_all([donkey26, flight1_donkey26])

    donkey27 = Tournaments(
        name="Donkey's Annual '27",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2027,3,9,10)
    )
    flight1_donkey27 = Flights(
        start_at=datetime(2027,3,9,10),
        tournament= donkey27,
        day=1
    )
    db.session.add_all([donkey27, flight1_donkey27])

    donkey28 = Tournaments(
        name="Donkey's Annual '28",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2028,3,9,10)
    )
    flight1_donkey28 = Flights(
        start_at=now,
        tournament= donkey28,
        day=1
    )
    db.session.add_all([donkey28, flight1_donkey28])

    donkey29 = Tournaments(
        name="Donkey's Annual '29",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2029,3,9,10)
    )
    flight1_donkey29 = Flights(
        start_at=datetime(2029,3,9,10),
        tournament= donkey29,
        day=1
    )
    db.session.add_all([donkey29, flight1_donkey29])

    donkey30 = Tournaments(
        name="Donkey's Annual '30",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2030,3,9,10)
    )
    flight1_donkey30 = Flights(
        start_at=datetime(2030,3,9,10),
        tournament= donkey30,
        day=1
    )
    db.session.add_all([donkey30, flight1_donkey30])


    db.session.commit()