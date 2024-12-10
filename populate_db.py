from app import app, db
from app.models import Saree

# Use Flask app context to interact with the database
with app.app_context():
    # Clear the existing saree data
    Saree.query.delete()  # This will delete all rows in the Saree table
    db.session.commit()
    print("All existing sarees cleared!")
    
    # Add sample sarees to the database
    sarees = [
        Saree(
            name="Gadwal Saree 1", 
            description="Elegant gadwal saree 1.", 
            price=20, 
            stock=10, 
            category="gadwal", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733417569/Gadwal_Saree_1_ebbj3b.jpg"
        ),
        Saree(
            name="Gadwal Saree 2", 
            description="Elegant gadwal saree 2.", 
            price=25, 
            stock=5, 
            category="gadwal", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733417569/Gadwal_Saree_2_fvxdre.jpg"   
        ),
        Saree(
            name="Gadwal Saree 3", 
            description="Elegant gadwal saree 3.", 
            price=25, 
            stock=5, 
            category="gadwal", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733417569/Gadwal_Saree_3_ef3fvr.jpg"
        ),
        Saree(
            name="Gadwal Saree 4", 
            description="Elegant gadwal saree 4.", 
            price=25, 
            stock=5, 
            category="gadwal", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733417569/Gadwal_Saree_4_doaygs.jpg"
            
        ),
        Saree(
            name="Kora Saree 1",
            description="Gorgeous kora saree 1.", 
            price=25, 
            stock=5, 
            category="kora", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733418982/Kora_Saree_1_lsuz3f.jpg"
               
        ),
        Saree(
            name="Kora Saree 2", 
            description="Gorgeous kora saree 2.", 
            price=25, 
            stock=5, 
            category="kora", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733418981/Kora_Saree_2_nnae4g.jpg"
        ),
        Saree(
            name="Kora Saree 3", 
            description="Gorgeous kora saree 3.", 
            price=25, 
            stock=5, 
            category="kora", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733418981/Kora_Saree_3_rtkse0.jpg"
        ),
        Saree(
            name="Kora Saree 4", 
            description="Gorgeous kora saree 4.", 
            price=25, 
            stock=5, 
            category="kora", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733418983/Kora_Saree_4_exgjwy.jpg"
        ),
        Saree(
            name="Kora Saree 5",
            description="Gorgeous kora saree 5.", 
            price=25, 
            stock=5, 
            category="kora", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733418983/Kora_Saree_5_hxixwj.jpg"
        ),
        Saree(
            name="Kora Saree 6", 
            description="Gorgeous kora saree 6.", 
            price=25, 
            stock=5, 
            category="kora", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733418984/Kora_Saree_6_oih7jm.jpg"
        ),
        Saree(
            name="Party Wear Saree 1", 
            description="Stunning partywear saree 1.", 
            price=25, 
            stock=5, 
            category="partywear", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733422332/PW_Saree_1_h9fkt9.jpg"),
        Saree(
            name="Party Wear Saree 2", 
            description="Stunning partywear saree 2.", 
            price=25, 
            stock=5, 
            category="partywear", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733422333/PW_Saree_2_vo7ham.jpg"),
        Saree(
            name="Party Wear Saree 3", 
            description="Stunning partywear saree 3.", 
            price=25, 
            stock=5, 
            category="partywear", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733422331/PW_Saree_3_jloq0s.jpg"),
        Saree(
            name="Party Wear Saree 4",
            description="Stunning partywear saree 4.", 
            price=25, 
            stock=5, 
            category="partywear", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733422331/PW_Saree_4_s30wpu.jpg"
        ),
        Saree(
            name="Party Wear Saree 5", 
            description="Stunning partywear saree 5.", 
            price=25, 
            stock=5, 
            category="partywear",
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733422334/PW_Saree_5_kknybd.jpg"
        ),
        Saree(
            name="Party Wear Saree 6", 
            description="Stunning partywear saree 6.", 
            price=25, 
            stock=5, 
            category="partywear",
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733422330/PW_Saree_6_akqk5c.jpg"
        ),
        Saree(
            name="Silk Saree 1", 
            description="Luxurious silk saree 1.", 
            price=25, 
            stock=5,
            category="silk", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733425309/Silk_Saree_1_tafuoi.jpg"
        ),
        Saree(
            name="Silk Saree 2", 
            description="Luxurious silk saree 2.", 
            price=25, 
            stock=5, 
            category="silk", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733425312/Silk_Saree_2_mkeeik.jpg"
        ),
        Saree(
            name="Silk Saree 3", 
            description="Luxurious silk saree 3.", 
            price=25, 
            stock=5, 
            category="silk", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733425312/Silk_Saree_3_rzdico.jpg"
        ),
        Saree(
            name="Silk Saree 4", 
            description="Luxurious silk saree 4.", 
            price=25, 
            stock=5, 
            category="silk", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733425310/Silk_Saree_4_eq3yr8.jpg"
        ),
        Saree(
            name="Silk Saree 5", 
            description="Luxurious silk saree 5.", 
            price=25, 
            stock=5, 
            category="silk", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733425310/Silk_Saree_5_c9g0ys.jpg"
        ),
        Saree(
            name="Silk Saree 6", 
            description="Luxurious silk saree 6.", 
            price=25, 
            stock=5, 
            category="silk", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733425314/Silk_Saree_6_txztqw.jpg"
        ),
        Saree(
            name="Silk Saree 7", 
            description="Luxurious silk saree 7.", 
            price=25, 
            stock=5, 
            category="silk", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733425314/Silk_Saree_7_vuwtcs.jpg"
        ),
        Saree(
            name="Silk Saree 8", 
            description="Luxurious silk saree 8.", 
            price=25, 
            stock=5, 
            category="silk", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733425316/Silk_Saree_8_vrlkaz.jpg"
        ),
        Saree(
            name="Georgette Saree 1", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="georgette", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733428695/Georgette_Saree_1_elqv40.jpg"
        ),
        Saree(
            name="Georgette Saree 2", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="georgette", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733428710/Georgette_Saree_5_esfitm.jpg"
        ),
        Saree(
            name="Georgette Saree 3", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="georgette", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733428713/Georgette_Saree_8_zprffy.jpg"
        ),
        Saree(
            name="Floral Lehenga 1", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="floral", 
            product_type="lehengas", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733430975/Lehenga_1_zj1jsg.jpg"
        ),
        Saree(
            name="Floral Lehenga 2", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="floral", 
            product_type="lehengas", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733430974/Lehenga_2_sa4gkw.jpg"
        ),
        Saree(
            name="Floral Lehenga 3", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="floral", 
            product_type="lehengas", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733431527/Lehenga_3_uqlzt9.jpg"
        ),
        Saree(
            name="Floral Lehenga 4", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="floral", 
            product_type="lehengas", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733431528/Lehenga_4_gexv6l.jpg"
        ),
        Saree(
            name="Chaniyacholi 1", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="chaniyacholi", 
            product_type="lehengas", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733445686/Chaniyacholi_1_lwvsp9.jpg"
        ),
        Saree(
            name="Chaniyacholi 2", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="chaniyacholi", 
            product_type="lehengas", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733445686/Chaniyacholi_2_l6lo81.jpg"
        ),
        Saree(
            name="Chaniyacholi 3", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="chaniyacholi", 
            product_type="lehengas", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733445687/Chaniyacholi_3_d6kjkl.jpg"
        ),
        Saree(
            name="Salwar 1", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="salwar", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733587527/Salwar_1_ijeq8l.jpg"
        ),
        Saree(
            name="Salwar 2", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="salwar", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733587527/Salwar_2_eapy3z.jpg"
        ),
        Saree(
            name="Salwar 3", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="salwar", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733587527/Salwar_3_if45o3.jpg"
        ),
        Saree(
            name="Salwar 4", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="salwar", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733587528/Salwar_5_t5y2vv.jpg"
        ),
        Saree(
            name="Salwar 5", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="salwar", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733587528/Salwar_6_nz7wwl.jpg"
        ),

        Saree(
            name="Kurti 1", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="kurtis", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733588044/Kurta_1_zd18r5.jpg"
        ),
        Saree(
            name="Kurti 2", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="kurtis", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733588044/Kurta_2_u574vd.jpg"
        ),
        Saree(
            name="Kurti 3", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="kurtis", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733588044/Kurta_3_jphcoe.jpg"
        ),
        Saree(
            name="Kurti 4", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="kurtis", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733588044/Kurta_4_knpqhj.jpg"
        ),
        Saree(
            name="Kurti 5", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="kurtis", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733588044/Kurta_5_lcxebb.jpg"
        ),
        Saree(
            name="Kurti 6", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="kurtis", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733588044/Kurta_6_yr9kbf.jpg"
        ),
        Saree(
            name="Blouse 1", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="blouses", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733588465/Blouse_1_knswca.jpg"
        ),
        Saree(
            name="Blouse 2", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="blouses", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733588464/Blouse_2_ufdx09.jpg"
        ),
        Saree(
            name="Blouse 3", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="blouses", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733588465/Blouse_3_ajmiue.jpg"
        ),
        Saree(
            name="Blouse 4", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="blouses", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733588464/Blouse_4_ayzn1k.jpg"
        ),
        Saree(
            name="Blouse 5", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="blouses", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733588465/Blouse_5_xbovfk.jpg"
        ),
        Saree(
            name="Blouse 6", 
            description="Luxurious silk saree.", 
            price=25, 
            stock=5, 
            category="blouses", 
            product_type="women", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733588465/Blouse_6_mvudtm.jpg"
        ),



        Saree(
            name=" Traditional Men 1", 
            description="Traditional Men Kurta 1.", 
            price=25, 
            stock=5, 
            category="traditionals", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733709487/Kurta_1_wdnbc8.jpg"
        ),
        Saree(
            name="Traditional Men 2", 
            description="Traditional Men Kurta 2.", 
            price=25, 
            stock=5, 
            category="traditionals", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733709487/Kurta_2_g0nlz1.jpg"
        ),
        Saree(
            name="Traditional Men 3", 
            description="Traditional Men Kurta 3.", 
            price=25, 
            stock=5, 
            category="traditionals", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733709486/Kurta_3_gdsz9j.jpg"
        ),
        Saree(
            name="Traditional Men 4", 
            description="Traditional Men Kurta 4.", 
            price=25, 
            stock=5, 
            category="traditionals", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733709486/Kurta_4_fseqcs.jpg"
        ),
        Saree(
            name="Traditional Men 5", 
            description="Traditional Men Kurta 5.", 
            price=25, 
            stock=5, 
            category="traditionals", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733709486/Kurta_5_lhkxxs.jpg"
        ),
        Saree(
            name="Traditional Men 6", 
            description="Traditional Men Kurta 6.", 
            price=25, 
            stock=5, 
            category="traditionals", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733709486/Kurta_6_ihoj7j.jpg"
        ),
        Saree(
            name="Traditional Men 7", 
            description="Traditional Men Kurta 7.", 
            price=25, 
            stock=5, 
            category="traditionals", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733709486/Kurta_7_zzf8zc.jpg"
        ),
        Saree(
            name="Traditional Men 8", 
            description="Traditional Men Kurta 8.", 
            price=25, 
            stock=5, 
            category="traditionals", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733709486/Kurta_8_olppah.jpg"
        ),
         Saree(
            name="Traditional Men 9", 
            description="Traditional Men Kurta 9.", 
            price=25, 
            stock=5, 
            category="traditionals", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733709521/Kurta_9_sswylx.jpg"
        ),
         Saree(
            name="Traditional Men 10", 
            description="Traditional Men Kurta 10.", 
            price=25, 
            stock=5, 
            category="traditionals", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733709520/Kurta_10_usgdoz.jpg"
        ),
         Saree(
            name="Traditional Men 11", 
            description="Traditional Men Kurta 11.", 
            price=25, 
            stock=5, 
            category="traditionals", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733709520/Kurta_11_epaze6.jpg"
        ),
         Saree(
            name="Traditional Men 12", 
            description="Traditional Men Kurta 12.", 
            price=25, 
            stock=5, 
            category="traditionals", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733709520/Kurta_12_r4yh3j.jpg"
        ),
        Saree(
            name="Jamdani Men 1", 
            description="Traditional Men Kurta 12.", 
            price=25, 
            stock=5, 
            category="jamdanis", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733753243/Jamdani_1_go4ktv.jpg"
        ),
        Saree(
            name="Jamdani Men 2", 
            description="Traditional Men Kurta 12.", 
            price=25, 
            stock=5, 
            category="jamdanis", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733753242/Jamdani_2_xnhelf.jpg"
        ),
        Saree(
            name="Jamdani Men 3", 
            description="Traditional Men Kurta 12.", 
            price=25, 
            stock=5, 
            category="jamdanis", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733753242/Jamdani_3_bcjov9.jpg"
        ),
        Saree(
            name="Jamdani Men 4", 
            description="Traditional Men Kurta 12.", 
            price=25, 
            stock=5, 
            category="jamdanis", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733753241/Jamdani_4_ybmoep.jpg"
        ),
        Saree(
            name="Jamdani Men 5", 
            description="Traditional Men Kurta 12.", 
            price=25, 
            stock=5, 
            category="jamdanis", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733753241/Jamdani_5_j1g9sd.jpg"
        ),
        Saree(
            name="Jamdani Men 6", 
            description="Traditional Men Kurta 12.", 
            price=25, 
            stock=5, 
            category="jamdanis", 
            product_type="men", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733753241/Jamdani_6_cuhxfs.jpg"
        ),

        Saree(
            name="Silk Saree 9",
            description="Traditional Men Kurta 12.", 
            price=95, 
            stock=10, 
            category="silk", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733790026/Silk_9_zgbigf.jpg"

        ),
        Saree(
            name="Partywear 7",
            description="Traditional Men Kurta 12.", 
            price=95, 
            stock=10, 
            category="partywear", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733790326/Partywear_7_cykodn.jpg"

        ),
        Saree(
            name="Partywear 8",
            description="Traditional Men Kurta 12.", 
            price=95, 
            stock=10, 
            category="partywear", 
            product_type="sarees", 
            image_url="https://res.cloudinary.com/dpar2oaev/image/upload/v1733790326/Partywear_8_aaflvo.jpg"

        )
        
        

    

    ]

    # Add sarees to the session and commit to save them
    db.session.add_all(sarees)
    db.session.commit()

    print("Database has been populated with sample data!")