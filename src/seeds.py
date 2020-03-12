import actions
from models import db, Users, Profiles, Tournaments, Swaps, Flights, Buy_ins, Transactions, Devices
from datetime import datetime, timedelta
from utils import sha256


def run():
         

    Devices.query.delete()
    Transactions.query.delete()
    Buy_ins.query.delete()
    Swaps.query.delete()
    Flights.query.delete()
    Tournaments.query.delete()
    Profiles.query.delete()
    Users.query.delete()

    db.session.execute("ALTER SEQUENCE users_id_seq RESTART")
    db.session.execute("ALTER SEQUENCE tournaments_id_seq RESTART WITH 1000")
    db.session.execute("ALTER SEQUENCE flights_id_seq RESTART WITH 1")
    db.session.execute("ALTER SEQUENCE buy_ins_id_seq RESTART")
    db.session.execute("ALTER SEQUENCE swaps_id_seq RESTART")
    db.session.execute("ALTER SEQUENCE transactions_id_seq RESTART")
    db.session.execute("ALTER SEQUENCE devices_id_seq RESTART")

    db.session.commit()


    actions.load_tournament_file()

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
        user=lou,
        roi_rating=78.3,
        swap_rating=5,
        total_swaps=275
    )
    db.session.add(lou)
    db.session.add( Transactions(
        coins=100,
        user=lou
    ))

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
        user=cary,
        roi_rating=34.8,
        swap_rating=4.3,
        total_swaps=198
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
        user=kate,
        roi_rating=23.7,
        swap_rating=5,
        total_swaps=143
    )
    db.session.add(kate)
    db.session.add( Transactions(
        coins=10,
        user=kate
    ))

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
        user=nikita,
        roi_rating=50.1,
        swap_rating=3.9,
        total_swaps=237
    )
    db.session.add(nikita)
    db.session.add( Transactions(
        coins=10,
        user=nikita
    ))

    brian = Users(
        email='brooklynbman@yahoo.com',
        password=sha256('Brooklyn1'),
        status='valid'
    )
    db.session.add(brian)
    brian = Profiles(
        first_name='Brian', 
        last_name='Gelrod',
        nickname='',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=239802',
        profile_pic_url='https://drive.google.com/open?id=1Y4OuXV1iunEth9TjVogE9w1t71_08AgG',
        user=brian,
        roi_rating=37.4,
        swap_rating=4.9,
        total_swaps=48
    )
    db.session.add(brian)
    db.session.add( Transactions(
        coins=10,
        user=brian
    ))

    bobby = Users(
        email='leff1117@aol.com',
        password=sha256('eatme'),
        status='valid'
    )
    db.session.add(bobby)
    bobby = Profiles(
        first_name='Bobby', 
        last_name='Leff',
        nickname='',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=187837',
        profile_pic_url='https://drive.google.com/open?id=1byJp9yhroNrj_kYJE1Lu_QQwApXCffR6',
        user=bobby,
        roi_rating=60.0,
        swap_rating=5.0,
        total_swaps=103
    )
    db.session.add(bobby)
    db.session.add( Transactions(
        coins=10,
        user=bobby
    ))

    perry = Users(
        email='perry1830@msn.com',
        password=sha256('Kobe$$'),
        status='valid'
    )
    db.session.add(perry)
    perry = Profiles(
        first_name='Perry', 
        last_name='Shiao',
        nickname='',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=371190',
        profile_pic_url='https://drive.google.com/open?id=1h7u3W0OUd1LwCN3LD2b-8qlScEFLIbRu',
        user=perry,
        roi_rating=38.2,
        swap_rating=4.5,
        total_swaps=175
    )
    db.session.add(perry)
    db.session.add( Transactions(
        coins=10,
        user=perry
    ))

    neal = Users(
        email='neal_corcoran@yahoo.com',
        password=sha256('Brooklyn1'),
        status='valid'
    )
    db.session.add(neal)
    neal = Profiles(
        first_name='Neal', 
        last_name='Corcoran',
        nickname='',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=506855',
        profile_pic_url='https://drive.google.com/open?id=1i9jVlQWK_sGFJ2zGlAFMamfbqrI2ZfpK',
        user=neal,
        roi_rating=62.4,
        swap_rating=3.5,
        total_swaps=97
    )
    db.session.add(neal)

    db.session.flush()

    ########################
    #     TOURNAMENTS
    ########################

    heartland = Tournaments(
        name='Hard Rock - RRPO #14 - NLH $2,000,000 Guaranteed - Day 2',
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
        name='PBKC - NLH $2,000 Guaranteed',
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
        name='Gulfstream - NLH $1,500 Guaranteed',
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
        name='Coconut Creek - NLH $5,000 Guaranteed w/$20 Bounties',
        address='Thunder Valley Casino Resort, 1200 Athens Ave',
        city='Lincoln',
        state='CA',
        zip_code='95648',
        latitude=38.904035,
        longitude=-121.295541,
        start_at=now - timedelta(days=2)
    )
    db.session.add(live)

    db.session.flush()

    ########################
    #       FLIGHTS
    ########################

    flight1_live = Flights(
        start_at=now,
        # end_at=now + timedelta(hours=5),
        tournament=live,
        day='1A'
    )
    flight2_live = Flights(
        start_at=now + timedelta(days=1),
        # end_at=now + timedelta(days=1, hours=5),
        tournament=live,
        day='1B'
    )
    db.session.add_all([flight1_live, flight2_live])


    flight1_heartland = Flights(
        start_at=datetime(2019,10,11,12),
        # end_at=datetime(2019,10,11,16),
        tournament=heartland,
        day='1'
    )
    flight2_heartland = Flights(
        start_at=datetime(2019,10,11,16),
        # end_at=datetime(2019,10,11,21),
        tournament=heartland,
        day='2'
    )
    db.session.add_all([flight1_heartland, flight2_heartland])


    flight1_stones = Flights(
        start_at=datetime(2019,9,30,12),
        # end_at=datetime(2019,9,30,15),
        tournament=stones,
        day='1'
    )
    flight2_stones = Flights(
        start_at=datetime(2019,9,30,15),
        # end_at=datetime(2019,9,30,21),
        tournament=stones,
        day='2'
    )
    flight3_stones = Flights(
        start_at=datetime(2019,10,1,12),
        # end_at=datetime(2019,10,1,21),
        tournament=stones,
        day='3'
    )
    db.session.add_all([flight1_stones, flight2_stones, flight3_stones])


    flight1_wpt = Flights(
        start_at=datetime(2019,10,2,12),
        # end_at=datetime(2019,10,2,22),
        tournament=wpt,
        day='1'
    )
    db.session.add(flight1_wpt)

    db.session.flush()

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

    db.session.flush()

    ########################
    #       BUY INS
    ########################

    db.session.add(Buy_ins(
        chips=1200,
        table='1',
        seat=2,
        user=lou,
        flight=flight1_live
    ))
    db.session.add(Buy_ins(
        chips=1200,
        table='1',
        seat=4,
        user=lou,
        flight=flight1_live
    ))
    db.session.add(Buy_ins(
        chips=500,
        table='7',
        seat=1,
        user=cary,
        flight=flight1_live
    ))
    db.session.add(Buy_ins(
        chips=250,
        table='1',
        seat=5,
        user=cary,
        flight=flight1_heartland
    ))
    db.session.add(Buy_ins(
        chips=1050,
        table='2',
        seat=3,
        user=lou,
        flight=flight2_heartland
    ))
    db.session.add(Buy_ins(
        chips=900,
        table='4',
        seat=5,
        user=kate,
        flight=flight2_heartland
    ))
    db.session.add(Buy_ins(
        chips=500,
        table='3',
        seat=2,
        user=cary,
        flight=flight2_live
    ))
    db.session.add(Buy_ins(
        chips=1000,
        table='2',
        seat=2,
        user=kate,
        flight=flight2_live
    ))
    db.session.add(Buy_ins(
        chips=300,
        table='2',
        seat=2,
        user=kate,
        flight=flight2_live
    ))  
    db.session.add(Buy_ins(
        chips=700,
        table='3',
        seat=1,
        user=nikita,
        flight=flight2_live
    ))

    db.session.flush()

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

    db.session.flush()

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
        start_at=newvegas.start_at,
        tournament=newvegas,
        day='1A'
    )
    flight2_newvegas = Flights(
        start_at=datetime(2281,10,11,10) + timedelta(hours=6),
        tournament=newvegas,
        day='1B'
    )
    db.session.add_all([newvegas, flight1_newvegas, flight2_newvegas])


    #######################
    #   UPCOMING BUYINS
    #######################
    
    db.session.add(Buy_ins(         
        chips=5000,         
        table='4',         
        seat=2,         
        user=lou,        
        flight=flight1_newvegas     
    ))
    db.session.add(Buy_ins(         
        chips=4000,         
        table='1',         
        seat=12,         
        user=cary,        
        flight=flight1_newvegas     
    ))
    db.session.add(Buy_ins(         
        chips=9000,         
        table='22',         
        seat=7,         
        user=kate,        
        flight=flight2_newvegas     
    ))
    db.session.add(Buy_ins(         
        chips=6000,         
        table='5',         
        seat=4,         
        user=nikita,        
        flight=flight2_newvegas     
    ))


    s1 = Swaps(
        tournament=newvegas,
        sender_user=lou,
        recipient_user=cary,
        percentage=11,
        due_at=(newvegas.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament= newvegas,
        sender_user=cary,
        recipient_user=lou,
        percentage=11,
        due_at=(newvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
    s1 = Swaps(
        tournament=newvegas,
        sender_user=lou,
        recipient_user=cary,
        percentage=50,
        due_at=(newvegas.start_at + timedelta(days=4)),
        status='rejected'
    )
    s2 = Swaps(
        tournament= newvegas,
        sender_user=cary,
        recipient_user=lou,
        percentage=50,
        due_at=(newvegas.start_at + timedelta(days=4)),
        status='rejected',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

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

    db.session.flush()

    ######################
    #   PAST TOURNAMENT
    ######################

    oldvegas = Tournaments(
        name='RRPO #21 - NLH $100,000 Guaranteed - Day 1A',
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
        # end_at=now + timedelta(days=1, hours=5),
        tournament=oldvegas,
        day='1'
    )
    db.session.add_all([oldvegas, flight1_oldvegas])

    db.session.flush()

    db.session.add(Buy_ins(         
        chips=7500,         
        table='14',         
        seat=12,         
        user=lou,
        winnings=1200,        
        flight=flight1_oldvegas     
    ))
    db.session.add(Buy_ins(         
        chips=4500,         
        table='21',         
        seat=1,         
        user=cary,
        winnings=4000,      
        flight=flight1_oldvegas     
    ))
    db.session.add(Buy_ins(         
        chips=5500,         
        table='1',         
        seat=7,         
        user=nikita,
        winnings=5000,       
        flight=flight1_oldvegas     
    ))
    db.session.add(Buy_ins(         
        chips=9000,         
        table='13',         
        seat=12,         
        user=kate,
        winnings=12000,     
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

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=lou,
        recipient_user=kate,
        percentage=20,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='rejected'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=kate,
        recipient_user=lou,
        percentage=20,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='rejected',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
    s1 = Swaps(
        tournament=oldvegas,
        sender_user=lou,
        recipient_user=cary,
        percentage=10,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=cary,
        recipient_user=lou,
        percentage=10,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    ##################
    # NEW TOURNAMENT
    ##################

    gamorrah = Tournaments(
        name='Coconut Creek - NLH $2,000 Guaranteed',
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
        # end_at=datetime(2281,10,11,16),
        tournament=gamorrah,
        day='1'
    )
    flight2_gamorrah = Flights(
        start_at=datetime(2281,10,11,16),
        # end_at=datetime(2281,10,11,21),
        tournament=gamorrah,
        day='2'
    )
    db.session.add_all([gamorrah, flight1_gamorrah, flight2_gamorrah])

    db.session.flush()

    db.session.add(Buy_ins(
        chips=13000,
        table='13',
        seat=3,
        user=kate,
        flight=flight1_gamorrah
    ))

    # TOURNAMENTS
    p2 = Tournaments(
        name='PBKC - NLH $2,500 Guaranteed',
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
        name='Hard Rock - RRPO #20 - 8 Max NLH $200,000 Guaranteed - Day 2',
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
        name='Hard Rock - RRPO #23 - High Roller NLH $1,000,000 Guaranteed - Day 1',
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
        name='Hard Rock - RRPO #24 - PLO',
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
        name='RRPO #21 - NLH $100,000 Guaranteed - Day 1B',
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
        name='Coconut Creek - NLH  $4,000 Guaranteed',
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
        name='Hard Rock - RRPO #25 - Six Max NLH',
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
        name='PBKC - NLH $2,000 Guaranteed',
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
        name='Gulfstream - Ladies NLH $1,500 Guaranteed',
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
        name='RRPO #21 - NLH $100,000 Guaranteed - Day 1C',
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
        name='The Big Easy - NLH $2,500 Guaranteed',
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

    db.session.flush()

    db.session.add(Buy_ins(
        chips=1200,
        table='1',
        seat=2,
        user=cary,
        flight=flight1_ocean
    ))


    # TWO
    royale = Tournaments(
        name='Isle - Omaha 8 or Better - $2,000 Guaranteed',
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

    db.session.flush()

    db.session.add(Buy_ins(
        chips=1200,
        table='1',
        seat=2,
        user=cary,
        flight=flight1_royale
    ))


    # THREE
    loathing = Tournaments(
        name='RRPO #21 - NLH $100,000 Guaranteed - Day 1D',
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

    db.session.flush()

    db.session.add(Buy_ins(
        chips=1200,
        table='1',
        seat=2,
        user=cary,
        flight=flight1_loathing
    ))


    # FOUR
    country = Tournaments(
        name='Coconut Creek - NLH Survivor $2,000 Guaranteed',
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

    db.session.flush()

    db.session.add(Buy_ins(
        chips=1200,
        table='1',
        seat=2,
        user=cary,
        flight=flight1_country
    ))


    # FIVE
    hangover = Tournaments(
        name='Hard Rock - RRPO #14 - NLH $2,000,000 Guaranteed - Day 4',
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

    db.session.flush()

    db.session.add(Buy_ins(
        chips=1200,
        table='1',
        seat=2,
        user=cary,
        flight=flight1_hangover
    ))


    # SIX
    king = Tournaments(
        name='Hard Rock - RRPO #26 - Seniors 50+ NLH',
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

    db.session.flush()

    db.session.add(Buy_ins(
        chips=1200,
        table='1',
        seat=2,
        user=cary,
        flight=flight1_king
    ))


    # SEVEN
    kakegurui = Tournaments(
        name='PBKC - NLH',
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

    db.session.flush()

    db.session.add(Buy_ins(
        chips=1200,
        table='1',
        seat=2,
        user=cary,
        flight=flight1_kakegurui
    ))


    # EIGHT
    ultimate = Tournaments(
        name='Hard Rock - RRPO #23 - High Roller NLH $1,000,000 Guaranteed - Day 2',
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

    db.session.flush()

    db.session.add(Buy_ins(
        chips=1200,
        table='1',
        seat=2,
        user=cary,
        flight=flight1_ultimate
    ))


    # NINE
    thankyou = Tournaments(
        name='RRPO #21 - NLH $100,000 Guaranteed - Day 1E',
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

    db.session.flush()

    db.session.add(Buy_ins(
        chips=1200,
        table='1',
        seat=2,
        user=cary,
        flight=flight1_thankyou
    ))


    # TEN
    battle = Tournaments(
        name='Isle - NLH $3,000 Guaranteed',
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

    db.session.flush()

    db.session.add(Buy_ins(
        chips=1200,
        table='1',
        seat=2,
        user=cary,
        flight=flight1_battle
    ))


    donkey21 = Tournaments(
        name="Kings Court Key - NLH $1,500 Guaranteed",
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
        day='1'
    )
    db.session.add_all([donkey21, flight1_donkey21])

    donkey22 = Tournaments(
        name="Coconut Creek - NLH  $4,000 Guaranteed w/$50 Bounties",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2022,3,12,10)
    )
    flight1_donkey22 = Flights(
        start_at=datetime(2022,3,12,10),
        tournament= donkey22,
        day='1'
    )
    db.session.add_all([donkey22, flight1_donkey22])

    donkey23 = Tournaments(
        name="Hard Rock - RRPO #27 - NLH",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2023,4,15,10)
    )
    flight1_donkey23 = Flights(
        start_at=datetime(2023,4,15,10),
        tournament= donkey23,
        day='1'
    )
    db.session.add_all([donkey23, flight1_donkey23])

    donkey24 = Tournaments(
        name="PBKC - NLH",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2024,5,20,10)
    )
    flight1_donkey24 = Flights(
        start_at=datetime(2024,5,20,10),
        tournament= donkey24,
        day='1'
    )
    db.session.add_all([donkey24, flight1_donkey24])

    donkey25 = Tournaments(
        name="Gulfstream - NLH $2,000 Guaranteed",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2025,5,21,10)
    )
    flight1_donkey25 = Flights(
        start_at=datetime(2025,5,21,10),
        tournament= donkey25,
        day='1'
    )
    db.session.add_all([donkey25, flight1_donkey25])

    donkey26 = Tournaments(
        name="RRPO #21 - NLH $100,000 Guaranteed - Day 1F",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2026,6,3,10)
    )
    flight1_donkey26 = Flights(
        start_at=datetime(2026,6,3,10),
        tournament= donkey26,
        day='1'
    )
    db.session.add_all([donkey26, flight1_donkey26])

    donkey27 = Tournaments(
        name="The Big Easy - NLH Shootout $2,500 Guaranteed",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2027,2,6,10)
    )
    flight1_donkey27 = Flights(
        start_at=datetime(2027,2,6,10),
        tournament= donkey27,
        day='1'
    )
    db.session.add_all([donkey27, flight1_donkey27])

    donkey28 = Tournaments(
        name="Isle - NLH Satellite for $200 seat(s)",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2028,10,1,10)
    )
    flight1_donkey28 = Flights(
        start_at=datetime(2028,10,1,10),
        tournament= donkey28,
        day='1'
    )
    db.session.add_all([donkey28, flight1_donkey28])

    donkey29 = Tournaments(
        name="Coconut Creek - Omaha Hi-Low $3,000 Guaranteed",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2029,1,2,10)
    )
    flight1_donkey29 = Flights(
        start_at=datetime(2029,1,2,10),
        tournament= donkey29,
        day='1'
    )
    db.session.add_all([donkey29, flight1_donkey29])

    donkey30 = Tournaments(
        name="Hard Rock - RRPO #14 - NLH $2,000,000 Guaranteed - Day 5",
        address='16849 102nd St SE',
        city='Hankinson',
        state='ND',
        zip_code='58041',
        latitude=45.9383,
        longitude=-96.8355,
        start_at=datetime(2030,9,8,10)
    )
    flight1_donkey30 = Flights(
        start_at=datetime(2030,9,8,10),
        tournament= donkey30,
        day='1'
    )
    db.session.add_all([donkey30, flight1_donkey30])

    db.session.flush()

    ## CURRENT TOURNAMENT 1 - live
    # CARY SWAPS
    s1 = Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=cary,
        percentage=2,
        status='agreed',
        due_at=(live.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=live,
        sender_user=cary,
        recipient_user=lou,
        percentage=2,
        status='agreed',
        due_at=(live.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=cary,
        percentage=5,
        status='agreed',
        due_at=(live.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=live,
        sender_user=cary,
        recipient_user=lou,
        percentage=3,
        status='agreed',
        due_at=(live.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=cary,
        percentage=15,
        status='canceled',
        due_at=(live.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=live,
        sender_user=cary,
        recipient_user=lou,
        percentage=15,
        status='canceled',
        due_at=(live.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    # KATE SWAPS
    s1 = Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=kate,
        percentage=15,
        status='agreed',
        due_at=(live.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=live,
        sender_user=kate,
        recipient_user=lou,
        percentage=15,
        status='agreed',
        due_at=(live.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=kate,
        percentage=15,
        status='rejected',
        due_at=(live.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=live,
        sender_user=kate,
        recipient_user=lou,
        percentage=15,
        status='rejected',
        due_at=(live.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    # NIKITA
    s1 = Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=nikita,
        percentage=15,
        status='counter_incoming',
        due_at=(live.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=live,
        sender_user=nikita,
        recipient_user=lou,
        percentage=15,
        status='pending',
        due_at=(live.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=nikita,
        percentage=1,
        status='agreed',
        due_at=(live.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=live,
        sender_user=nikita,
        recipient_user=lou,
        percentage=1,
        status='agreed',
        due_at=(live.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
    ## CURRENT TOURNAMENT 2 - newvegas
    # KATE SWAPS 
    s1 = Swaps(
        tournament=newvegas,
        sender_user=lou,
        recipient_user=kate,
        percentage=21,
        status='agreed',
        due_at=(newvegas.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament= newvegas,
        sender_user=kate,
        recipient_user=lou,
        percentage=21,
        status='agreed',
        due_at=(newvegas.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=newvegas,
        sender_user=lou,
        recipient_user=kate,
        percentage=10,
        status='agreed',
        due_at=(newvegas.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament= newvegas,
        sender_user=kate,
        recipient_user=lou,
        percentage=9,
        status='agreed',
        due_at=(newvegas.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
    # NIKITA SWAPS 
    s1 = Swaps(
        tournament=newvegas,
        sender_user=lou,
        recipient_user=nikita,
        percentage=1,
        status='canceled',
        due_at=(newvegas.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament= newvegas,
        sender_user=nikita,
        recipient_user=lou,
        percentage=1,
        status='canceled',
        due_at=(newvegas.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    db.session.flush()



    ##############################################
    ##############################################
    ##############################################
    # SWAP POKER BETA SEEDS

    # 1 Neal

	# Tournament 1

	# NEAL BUYIN

    db.session.add(Buy_ins(
        chips=1500,
        table='213',
        seat=2,
        user=neal,
        flight=flight1_royale
    ))

    # OTHER BUYINS

    db.session.add(Buy_ins(
        chips=2300,
        table='3',
        seat=2,
        user=cary,
        flight=flight1_royale
    ))

    db.session.add(Buy_ins(
        chips=10000,
        table='43',
        seat=5,
        user=kate,
        flight=flight1_royale
    ))

    db.session.add(Buy_ins(
        chips=8000,
        table='33',
        seat=2,
        user=nikita,
        flight=flight1_royale
    ))

    # SWAPS

    # CARY SWAPS

    s1 = Swaps(
        tournament=royale,
        sender_user=neal,
        recipient_user=cary,
        percentage=2,
        status='agreed',
        due_at=(royale.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=royale,
        sender_user=cary,
        recipient_user=neal,
        percentage=2,
        status='agreed',
        due_at=(royale.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=royale,
        sender_user=neal,
        recipient_user=cary,
        percentage=5,
        status='agreed',
        due_at=(royale.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=royale,
        sender_user=cary,
        recipient_user=neal,
        percentage=3,
        status='agreed',
        due_at=(royale.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=royale,
        sender_user=neal,
        recipient_user=cary,
        percentage=15,
        status='canceled',
        due_at=(royale.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=royale,
        sender_user=cary,
        recipient_user=neal,
        percentage=15,
        status='canceled',
        due_at=(royale.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    # KATE SWAPS

    s1 = Swaps(
        tournament=royale,
        sender_user=neal,
        recipient_user=kate,
        percentage=15,
        status='agreed',
        due_at=(royale.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=royale,
        sender_user=kate,
        recipient_user=neal,
        percentage=15,
        status='agreed',
        due_at=(royale.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=royale,
        sender_user=neal,
        recipient_user=kate,
        percentage=15,
        status='rejected',
        due_at=(royale.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=royale,
        sender_user=kate,
        recipient_user=neal,
        percentage=15,
        status='rejected',
        due_at=(royale.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    # NIKITA SWAPS

    s1 = Swaps(
        tournament=royale,
        sender_user=neal,
        recipient_user=nikita,
        percentage=15,
        status='counter_incoming',
        due_at=(royale.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=royale,
        sender_user=nikita,
        recipient_user=neal,
        percentage=15,
        status='pending',
        due_at=(royale.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=royale,
        sender_user=neal,
        recipient_user=nikita,
        percentage=1,
        status='agreed',
        due_at=(royale.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=royale,
        sender_user=nikita,
        recipient_user=neal,
        percentage=1,
        status='agreed',
        due_at=(royale.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])



	# Tournament 2

	# NEAL BUYIN

    db.session.add(Buy_ins(
        chips=12500,
        table='4',
        seat=1,
        user=neal,
        flight=flight1_king
    ))

	# OTHER BUYINS

    db.session.add(Buy_ins(
        chips=3500,
        table='33',
        seat=4,
        user=cary,
        flight=flight1_king
    ))

    db.session.add(Buy_ins(
        chips=3000,
        table='3',
        seat=4,
        user=kate,
        flight=flight1_king
    ))

    db.session.add(Buy_ins(
        chips=8500,
        table='3',
        seat=6,
        user=nikita,
        flight=flight1_king
    ))

    # SWAPS

    # CARY SWAPS

    s1 = Swaps(
        tournament=king,
        sender_user=neal,
        recipient_user=cary,
        percentage=11,
        due_at=(king.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament=king,
        sender_user=cary,
        recipient_user=neal,
        percentage=11,
        due_at=(king.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
    s1 = Swaps(
        tournament=king,
        sender_user=neal,
        recipient_user=cary,
        percentage=50,
        due_at=(king.start_at + timedelta(days=4)),
        status='rejected'
    )
    s2 = Swaps(
        tournament=king,
        sender_user=cary,
        recipient_user=neal,
        percentage=50,
        due_at=(king.start_at + timedelta(days=4)),
        status='rejected',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

	# KATE SWAPS 
    s1 = Swaps(
        tournament=king,
        sender_user=neal,
        recipient_user=kate,
        percentage=21,
        status='agreed',
        due_at=(king.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=king,
        sender_user=kate,
        recipient_user=neal,
        percentage=21,
        status='agreed',
        due_at=(king.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=king,
        sender_user=neal,
        recipient_user=kate,
        percentage=10,
        status='agreed',
        due_at=(king.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=king,
        sender_user=kate,
        recipient_user=neal,
        percentage=9,
        status='agreed',
        due_at=(king.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
    # NIKITA SWAPS 

    s1 = Swaps(
        tournament=king,
        sender_user=neal,
        recipient_user=nikita,
        percentage=1,
        status='canceled',
        due_at=(king.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=king,
        sender_user=nikita,
        recipient_user=neal,
        percentage=1,
        status='canceled',
        due_at=(king.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    # Past Tournament

    db.session.add(Buy_ins(         
        chips=7500,         
        table='142',         
        seat=12,         
        user=neal,
        winnings=12000,        
        flight=flight1_oldvegas     
    ))

    # SWAPS

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=neal,
        recipient_user=cary,
        percentage=5,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=cary,
        recipient_user=neal,
        percentage=3,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=neal,
        recipient_user=cary,
        percentage=6,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=cary,
        recipient_user=neal,
        percentage=8,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=oldvegas,
        sender_user=neal,
        recipient_user=nikita,
        percentage=5,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        paid=True
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=nikita,
        recipient_user=neal,
        percentage=7,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=oldvegas,
        sender_user=neal,
        recipient_user=kate,
        percentage=15,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='pending'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=kate,
        recipient_user=neal,
        percentage=17,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='incoming',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=neal,
        recipient_user=kate,
        percentage=20,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='rejected'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=neal,
        recipient_user=lou,
        percentage=20,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='rejected',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
  
    # 2 Brian

	# Tournament 1

	# BRIAN BUYIN
  	
    db.session.add(Buy_ins(
        chips=1200,
        table='721',
        seat=2,
        user=brian,
        flight=flight1_loathing
    ))

    # OTHER BUYINS

    db.session.add(Buy_ins(
        chips=2300,
        table='3',
        seat=2,
        user=cary,
        flight=flight1_loathing
    ))

    db.session.add(Buy_ins(
        chips=10000,
        table='43',
        seat=5,
        user=kate,
        flight=flight1_loathing
    ))

    db.session.add(Buy_ins(
        chips=8000,
        table='33',
        seat=2,
        user=nikita,
        flight=flight1_loathing
    ))

    # SWAPS

    # CARY SWAPS

    s1 = Swaps(
        tournament=loathing,
        sender_user=brian,
        recipient_user=cary,
        percentage=2,
        status='agreed',
        due_at=(loathing.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=loathing,
        sender_user=cary,
        recipient_user=brian,
        percentage=2,
        status='agreed',
        due_at=(loathing.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=loathing,
        sender_user=brian,
        recipient_user=cary,
        percentage=5,
        status='agreed',
        due_at=(loathing.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=loathing,
        sender_user=cary,
        recipient_user=brian,
        percentage=3,
        status='agreed',
        due_at=(loathing.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=loathing,
        sender_user=brian,
        recipient_user=cary,
        percentage=15,
        status='canceled',
        due_at=(loathing.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=loathing,
        sender_user=cary,
        recipient_user=brian,
        percentage=15,
        status='canceled',
        due_at=(loathing.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    # KATE SWAPS

    s1 = Swaps(
        tournament=loathing,
        sender_user=brian,
        recipient_user=kate,
        percentage=15,
        status='agreed',
        due_at=(loathing.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=loathing,
        sender_user=kate,
        recipient_user=brian,
        percentage=15,
        status='agreed',
        due_at=(loathing.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=loathing,
        sender_user=brian,
        recipient_user=kate,
        percentage=15,
        status='rejected',
        due_at=(loathing.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=loathing,
        sender_user=kate,
        recipient_user=brian,
        percentage=15,
        status='rejected',
        due_at=(loathing.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    # NIKITA SWAPS

    s1 = Swaps(
        tournament=loathing,
        sender_user=brian,
        recipient_user=nikita,
        percentage=15,
        status='counter_incoming',
        due_at=(loathing.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=loathing,
        sender_user=nikita,
        recipient_user=brian,
        percentage=15,
        status='pending',
        due_at=(loathing.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=loathing,
        sender_user=brian,
        recipient_user=nikita,
        percentage=1,
        status='agreed',
        due_at=(loathing.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=loathing,
        sender_user=nikita,
        recipient_user=brian,
        percentage=1,
        status='agreed',
        due_at=(loathing.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])





	# Tournament 2

	# BRIAN BUYIN

    db.session.add(Buy_ins(
        chips=1200,
        table='172',
        seat=2,
        user=brian,
        flight=flight1_kakegurui
    ))

    # OTHER BUYINS

    db.session.add(Buy_ins(
        chips=3500,
        table='33',
        seat=4,
        user=cary,
        flight=flight1_kakegurui
    ))

    db.session.add(Buy_ins(
        chips=3000,
        table='3',
        seat=4,
        user=kate,
        flight=flight1_kakegurui
    ))

    db.session.add(Buy_ins(
        chips=8500,
        table='3',
        seat=6,
        user=nikita,
        flight=flight1_kakegurui
    ))


    # SWAPS

    # CARY SWAPS

    s1 = Swaps(
        tournament=kakegurui,
        sender_user=brian,
        recipient_user=cary,
        percentage=11,
        due_at=(kakegurui.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament=kakegurui,
        sender_user=cary,
        recipient_user=brian,
        percentage=11,
        due_at=(kakegurui.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
    s1 = Swaps(
        tournament=kakegurui,
        sender_user=brian,
        recipient_user=cary,
        percentage=50,
        due_at=(kakegurui.start_at + timedelta(days=4)),
        status='rejected'
    )
    s2 = Swaps(
        tournament=kakegurui,
        sender_user=cary,
        recipient_user=brian,
        percentage=50,
        due_at=(kakegurui.start_at + timedelta(days=4)),
        status='rejected',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

	# KATE SWAPS 
    s1 = Swaps(
        tournament=kakegurui,
        sender_user=brian,
        recipient_user=kate,
        percentage=21,
        status='agreed',
        due_at=(kakegurui.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=kakegurui,
        sender_user=kate,
        recipient_user=brian,
        percentage=21,
        status='agreed',
        due_at=(kakegurui.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=kakegurui,
        sender_user=brian,
        recipient_user=kate,
        percentage=10,
        status='agreed',
        due_at=(kakegurui.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=kakegurui,
        sender_user=kate,
        recipient_user=brian,
        percentage=9,
        status='agreed',
        due_at=(kakegurui.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
    # NIKITA SWAPS 

    s1 = Swaps(
        tournament=kakegurui,
        sender_user=brian,
        recipient_user=nikita,
        percentage=1,
        status='canceled',
        due_at=(kakegurui.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=kakegurui,
        sender_user=nikita,
        recipient_user=brian,
        percentage=1,
        status='canceled',
        due_at=(kakegurui.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])




    # Past Tournament

    # BRIAN BUYIN

    db.session.add(Buy_ins(         
        chips=7500,         
        table='164',         
        seat=12,         
        user=brian,
        winnings=3000,        
        flight=flight1_oldvegas     
    ))


    # SWAPS

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=brian,
        recipient_user=cary,
        percentage=5,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=cary,
        recipient_user=brian,
        percentage=3,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=brian,
        recipient_user=cary,
        percentage=6,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=cary,
        recipient_user=brian,
        percentage=8,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=oldvegas,
        sender_user=brian,
        recipient_user=nikita,
        percentage=5,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        paid=True
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=nikita,
        recipient_user=brian,
        percentage=7,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=oldvegas,
        sender_user=brian,
        recipient_user=kate,
        percentage=15,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='pending'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=kate,
        recipient_user=brian,
        percentage=17,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='incoming',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=brian,
        recipient_user=kate,
        percentage=20,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='rejected'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=kate,
        recipient_user=brian,
        percentage=20,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='rejected',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    # 3 Perry

	# Tournament 1

	# PERRY BUYIN

    db.session.add(Buy_ins(
        chips=1200,
        table='126',
        seat=2,
        user=perry,
        flight=flight1_country
    ))

    # OTHER BUYINS

    db.session.add(Buy_ins(
        chips=2300,
        table='3',
        seat=2,
        user=cary,
        flight=flight1_country
    ))

    db.session.add(Buy_ins(
        chips=10000,
        table='43',
        seat=5,
        user=kate,
        flight=flight1_country
    ))

    db.session.add(Buy_ins(
        chips=8000,
        table='33',
        seat=2,
        user=nikita,
        flight=flight1_country
    ))

    # SWAPS

    # CARY SWAPS

    s1 = Swaps(
        tournament=country,
        sender_user=perry,
        recipient_user=cary,
        percentage=2,
        status='agreed',
        due_at=(country.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=country,
        sender_user=cary,
        recipient_user=perry,
        percentage=2,
        status='agreed',
        due_at=(country.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=country,
        sender_user=perry,
        recipient_user=cary,
        percentage=5,
        status='agreed',
        due_at=(country.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=country,
        sender_user=cary,
        recipient_user=perry,
        percentage=3,
        status='agreed',
        due_at=(country.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=country,
        sender_user=perry,
        recipient_user=cary,
        percentage=15,
        status='canceled',
        due_at=(country.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=country,
        sender_user=cary,
        recipient_user=perry,
        percentage=15,
        status='canceled',
        due_at=(country.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    # KATE SWAPS

    s1 = Swaps(
        tournament=country,
        sender_user=perry,
        recipient_user=kate,
        percentage=15,
        status='agreed',
        due_at=(country.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=country,
        sender_user=kate,
        recipient_user=perry,
        percentage=15,
        status='agreed',
        due_at=(country.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=country,
        sender_user=perry,
        recipient_user=kate,
        percentage=15,
        status='rejected',
        due_at=(country.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=country,
        sender_user=kate,
        recipient_user=perry,
        percentage=15,
        status='rejected',
        due_at=(country.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    # NIKITA SWAPS

    s1 = Swaps(
        tournament=country,
        sender_user=perry,
        recipient_user=nikita,
        percentage=15,
        status='counter_incoming',
        due_at=(country.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=country,
        sender_user=nikita,
        recipient_user=perry,
        percentage=15,
        status='pending',
        due_at=(country.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=country,
        sender_user=perry,
        recipient_user=nikita,
        percentage=1,
        status='agreed',
        due_at=(country.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=country,
        sender_user=nikita,
        recipient_user=perry,
        percentage=1,
        status='agreed',
        due_at=(country.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])




	# Tournament 2

	# PERRY BUYIN

    db.session.add(Buy_ins(
        chips=1200,
        table='13',
        seat=2,
        user=perry,
        flight=flight1_ultimate
    ))

    # OTHER BUYINS

    db.session.add(Buy_ins(
        chips=3500,
        table='33',
        seat=4,
        user=cary,
        flight=flight1_ultimate
    ))

    db.session.add(Buy_ins(
        chips=3000,
        table='3',
        seat=4,
        user=kate,
        flight=flight1_ultimate
    ))

    db.session.add(Buy_ins(
        chips=8500,
        table='3',
        seat=6,
        user=nikita,
        flight=flight1_ultimate
    ))

    # SWAPS

    # CARY SWAPS

    s1 = Swaps(
        tournament=ultimate,
        sender_user=perry,
        recipient_user=cary,
        percentage=11,
        due_at=(ultimate.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament=ultimate,
        sender_user=cary,
        recipient_user=perry,
        percentage=11,
        due_at=(ultimate.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
    s1 = Swaps(
        tournament=ultimate,
        sender_user=perry,
        recipient_user=cary,
        percentage=50,
        due_at=(ultimate.start_at + timedelta(days=4)),
        status='rejected'
    )
    s2 = Swaps(
        tournament=ultimate,
        sender_user=cary,
        recipient_user=perry,
        percentage=50,
        due_at=(ultimate.start_at + timedelta(days=4)),
        status='rejected',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

	# KATE SWAPS 
    s1 = Swaps(
        tournament=ultimate,
        sender_user=perry,
        recipient_user=kate,
        percentage=21,
        status='agreed',
        due_at=(ultimate.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=ultimate,
        sender_user=kate,
        recipient_user=perry,
        percentage=21,
        status='agreed',
        due_at=(ultimate.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=ultimate,
        sender_user=perry,
        recipient_user=kate,
        percentage=10,
        status='agreed',
        due_at=(ultimate.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=ultimate,
        sender_user=kate,
        recipient_user=perry,
        percentage=9,
        status='agreed',
        due_at=(ultimate.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
    # NIKITA SWAPS 

    s1 = Swaps(
        tournament=ultimate,
        sender_user=perry,
        recipient_user=nikita,
        percentage=1,
        status='canceled',
        due_at=(ultimate.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=ultimate,
        sender_user=nikita,
        recipient_user=perry,
        percentage=1,
        status='canceled',
        due_at=(ultimate.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


	# Past Tournament

	# PERRY BUYIN

    db.session.add(Buy_ins(         
        chips=7500,         
        table='814',         
        seat=12,         
        user=perry,
        winnings=10000,        
        flight=flight1_oldvegas     
    ))

    # SWAPS

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=perry,
        recipient_user=cary,
        percentage=5,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=cary,
        recipient_user=perry,
        percentage=3,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=perry,
        recipient_user=cary,
        percentage=6,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=cary,
        recipient_user=perry,
        percentage=8,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=oldvegas,
        sender_user=perry,
        recipient_user=nikita,
        percentage=5,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        paid=True
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=nikita,
        recipient_user=perry,
        percentage=7,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=oldvegas,
        sender_user=perry,
        recipient_user=kate,
        percentage=15,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='pending'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=kate,
        recipient_user=perry,
        percentage=17,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='incoming',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=perry,
        recipient_user=kate,
        percentage=20,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='rejected'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=kate,
        recipient_user=perry,
        percentage=20,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='rejected',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    # 4 Bobby

	# Tournament 1

	# BOBBY BUYIN

    db.session.add(Buy_ins(
        chips=1200,
        table='81',
        seat=2,
        user=bobby,
        flight=flight1_hangover
    ))

    # OTHER BUYINS

    db.session.add(Buy_ins(
        chips=2300,
        table='3',
        seat=2,
        user=cary,
        flight=flight1_hangover
    ))

    db.session.add(Buy_ins(
        chips=10000,
        table='43',
        seat=5,
        user=kate,
        flight=flight1_hangover
    ))

    db.session.add(Buy_ins(
        chips=8000,
        table='33',
        seat=2,
        user=nikita,
        flight=flight1_hangover
    ))

    # SWAPS

    s1 = Swaps(
        tournament=hangover,
        sender_user=bobby,
        recipient_user=cary,
        percentage=2,
        status='agreed',
        due_at=(hangover.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=hangover,
        sender_user=cary,
        recipient_user=bobby,
        percentage=2,
        status='agreed',
        due_at=(hangover.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=hangover,
        sender_user=bobby,
        recipient_user=cary,
        percentage=5,
        status='agreed',
        due_at=(hangover.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=hangover,
        sender_user=cary,
        recipient_user=bobby,
        percentage=3,
        status='agreed',
        due_at=(hangover.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=hangover,
        sender_user=bobby,
        recipient_user=cary,
        percentage=15,
        status='canceled',
        due_at=(hangover.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=hangover,
        sender_user=cary,
        recipient_user=bobby,
        percentage=15,
        status='canceled',
        due_at=(hangover.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    # KATE SWAPS

    s1 = Swaps(
        tournament=hangover,
        sender_user=bobby,
        recipient_user=kate,
        percentage=15,
        status='agreed',
        due_at=(hangover.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=hangover,
        sender_user=kate,
        recipient_user=bobby,
        percentage=15,
        status='agreed',
        due_at=(hangover.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=hangover,
        sender_user=bobby,
        recipient_user=kate,
        percentage=15,
        status='rejected',
        due_at=(hangover.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=hangover,
        sender_user=kate,
        recipient_user=bobby,
        percentage=15,
        status='rejected',
        due_at=(hangover.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    # NIKITA SWAPS

    s1 = Swaps(
        tournament=hangover,
        sender_user=bobby,
        recipient_user=nikita,
        percentage=15,
        status='counter_incoming',
        due_at=(hangover.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=hangover,
        sender_user=nikita,
        recipient_user=bobby,
        percentage=15,
        status='pending',
        due_at=(hangover.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=hangover,
        sender_user=bobby,
        recipient_user=nikita,
        percentage=1,
        status='agreed',
        due_at=(hangover.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=hangover,
        sender_user=nikita,
        recipient_user=bobby,
        percentage=1,
        status='agreed',
        due_at=(hangover.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


	# Tournament 2

	# BOBBY BUYIN

    db.session.add(Buy_ins(
        chips=1200,
        table='18',
        seat=2,
        user=bobby,
        flight=flight1_thankyou
    ))

    # OTHER BUYINS

    db.session.add(Buy_ins(
        chips=3500,
        table='33',
        seat=4,
        user=cary,
        flight=flight1_thankyou
    ))

    db.session.add(Buy_ins(
        chips=3000,
        table='3',
        seat=4,
        user=kate,
        flight=flight1_thankyou
    ))

    db.session.add(Buy_ins(
        chips=8500,
        table='3',
        seat=6,
        user=nikita,
        flight=flight1_thankyou
    ))

    # SWAPS

    # CARY SWAPS

    s1 = Swaps(
        tournament=thankyou,
        sender_user=bobby,
        recipient_user=cary,
        percentage=11,
        due_at=(thankyou.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament=thankyou,
        sender_user=cary,
        recipient_user=bobby,
        percentage=11,
        due_at=(thankyou.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
    s1 = Swaps(
        tournament=thankyou,
        sender_user=bobby,
        recipient_user=cary,
        percentage=50,
        due_at=(thankyou.start_at + timedelta(days=4)),
        status='rejected'
    )
    s2 = Swaps(
        tournament=thankyou,
        sender_user=cary,
        recipient_user=bobby,
        percentage=50,
        due_at=(thankyou.start_at + timedelta(days=4)),
        status='rejected',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

	# KATE SWAPS 
    s1 = Swaps(
        tournament=thankyou,
        sender_user=bobby,
        recipient_user=kate,
        percentage=21,
        status='agreed',
        due_at=(thankyou.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=thankyou,
        sender_user=kate,
        recipient_user=bobby,
        percentage=21,
        status='agreed',
        due_at=(thankyou.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=thankyou,
        sender_user=bobby,
        recipient_user=kate,
        percentage=10,
        status='agreed',
        due_at=(thankyou.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=thankyou,
        sender_user=kate,
        recipient_user=bobby,
        percentage=9,
        status='agreed',
        due_at=(thankyou.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    
    # NIKITA SWAPS 

    s1 = Swaps(
        tournament=thankyou,
        sender_user=bobby,
        recipient_user=nikita,
        percentage=1,
        status='canceled',
        due_at=(thankyou.start_at + timedelta(days=4))
    )
    s2 = Swaps(
        tournament=thankyou,
        sender_user=nikita,
        recipient_user=bobby,
        percentage=1,
        status='canceled',
        due_at=(thankyou.start_at + timedelta(days=4)),
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])



    #  Past Tournament

    # BOBBY BUYIN

    db.session.add(Buy_ins(         
        chips=7500,         
        table='184',         
        seat=12,         
        user=bobby,
        winnings=5000,        
        flight=flight1_oldvegas     
    ))


    # SWAPS

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=bobby,
        recipient_user=cary,
        percentage=5,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=cary,
        recipient_user=bobby,
        percentage=3,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=bobby,
        recipient_user=cary,
        percentage=6,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=cary,
        recipient_user=bobby,
        percentage=8,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=oldvegas,
        sender_user=bobby,
        recipient_user=nikita,
        percentage=5,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        paid=True
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=nikita,
        recipient_user=bobby,
        percentage=7,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='agreed',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])


    s1 = Swaps(
        tournament=oldvegas,
        sender_user=bobby,
        recipient_user=kate,
        percentage=15,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='pending'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=kate,
        recipient_user=bobby,
        percentage=17,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='incoming',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])

    s1 = Swaps(
        tournament=oldvegas,
        sender_user=bobby,
        recipient_user=kate,
        percentage=20,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='rejected'
    )
    s2 = Swaps(
        tournament= oldvegas,
        sender_user=kate,
        recipient_user=bobby,
        percentage=20,
        due_at=(oldvegas.start_at + timedelta(days=4)),
        status='rejected',
        counter_swap=s1
    )
    s1.counter_swap = s2
    db.session.add_all([s1, s2])
    ##############################################
    ##############################################
    ##############################################


    
    db.session.commit()
