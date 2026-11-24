import json
from backend.database import get_db, init_db

PRODUCTS = [
    {
        "id": 1,
        "slug": "royale-vanity-trunk",
        "name": "The Royale Vanity Trunk",
        "category": "Vanity Cases & Trunks",
        "category_slug": "vanity",
        "price": 3499.0,
        "original_price": 4999.0,
        "discount_percent": 30,
        "badge": "Bestseller",
        "rating": 4.9,
        "reviews_count": 128,
        "edition_tag": "Atelier Signature • Edition No. 04",
        "short_description": "Exquisite structured luxury vanity trunk case with fine grain leatherette texture and brushed champagne brass lock claps.",
        "description": "Crafted for the modern connoisseur, The Royale Vanity Trunk balances heirloom Indian leathercraft with contemporary boudoir architecture. Featuring modular plush velvet dividers, dedicated cosmetic brush loops, 24K brushed brass hardware, and dual side zipper security, it is tailored for both grand vanity desks and luxurious travels.",
        "material": "Top-tier Saffiano Eco-Leather (Supple & Water-Resistant)",
        "lining": "Ultra-plush Italian rose velvet with spill-proof wipeable base",
        "hardware": "Brushed 24k Champagne Brass Clasp with Protective Key Lock",
        "dimensions": "28cm (L) x 19cm (W) x 21cm (H)",
        "provenance": "Handcrafted by master artisans in Jaipur, India",
        "stock_quantity": 42,
        "is_featured": 1,
        "is_bestseller": 1,
        "is_new": 0,
        "colors": json.dumps([
            {"name": "Rose Gold & Cream", "hex": "#E5B5B8", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCE89CcKxs_5YuJkKe2LKS3Bq2PW-w8TwgOK9__ZynEr0_wpExwWDL7DR70PV26qAo8hCfjer75kA46NG88eozDTz26WKgCM1tK3lKq4luc6PcoSGlNZY2Q6tSYlEja9kNekr221PfbYBaGsFXs6uIpPz1TY591dSHgkDEbQjR-SBu7PKRtWVkQDsZLlACxH-I2y-Yp6PL0BiM0yiCMU3Dc1kUUz-hOGmtZNMMD2b0G"},
            {"name": "Pearl Ivory", "hex": "#E4E2DF", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCHoIz511UdCvPAYuysvWPFSjuI0lTgwf_38tipAg2_ojXOsM2jFUXXjEfLC3gH6e2RGNTi_vIJlpWThb5Dy8zyPO09-Hc1qPv6VLphbhHJPVakmTk-JVyZkA1iGgBF3lbvH3woeWx9KUYiwmfLgFBnpIawEcUc4tbXBBXy7Pa-I2EKFjZvLJr8L21vWRhZuDVQ2lvfql9WeT61BlOkIeS3eSsFbd9a8sK9wwOrGMzK"},
            {"name": "Onyx Noir", "hex": "#1B1C1A", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCnQcqbrZdUr0e747W4SJuyIDTe3HXH-dgbfCjRkxVDAO4-1U8r-zFU78pLD7YcFSrKlCqzBsD0hL9e2Pf2fTkmWF-nd0_2JknNytpPOoalfXA4PA6mJu-TzCdtlG018ApvgG1DalANn8vH2Hj_QGZz6hUNv9w5hMFxTak_HQFgUlvmd4iczhQMVmLNWaAuYF9_wqbNjOxeS-u4DEiDS9sFOjkyGC5Uii5r-djpFZa7"}
        ]),
        "images": json.dumps([
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCE89CcKxs_5YuJkKe2LKS3Bq2PW-w8TwgOK9__ZynEr0_wpExwWDL7DR70PV26qAo8hCfjer75kA46NG88eozDTz26WKgCM1tK3lKq4luc6PcoSGlNZY2Q6tSYlEja9kNekr221PfbYBaGsFXs6uIpPz1TY591dSHgkDEbQjR-SBu7PKRtWVkQDsZLlACxH-I2y-Yp6PL0BiM0yiCMU3Dc1kUUz-hOGmtZNMMD2b0G",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuDmz3aN28XRnxndlYo2pMv3zFDvVSjZct8ut3UwhURUvC4_Vh3VKDKcbHw-TlKnZVZBoW-3bjvt5IcKb904SH4viT9rFuzV6PET7h56AXAW6MOFdS7pIn3gObX_d9WFqhEBN2jO6-Dop73ozx5jlGSK8MV9u9ZjYcLfvKGwsKoWxnjTRGtbSQc5EUYBnN5YpYKXIzNY98Ml9BUeqCwlVTKRLYyGdEL_cUF2cNVaYnWy",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBSQx2mXx0cBnnXFXvks1SvgcNJb9ZMVhCwQiGQ2kIlggHOQvUaYwjeobvueC97ImvKmN_AR1HSjmFuU4uid4QvYfvsdHOej9aDUu2Vo7a7M2takD4WpzahVNwjUuzSZGgt_b8ORJolwRqbfg_8xgYcx0e9WpvLuxQIk5gS7ZJIs_nX_6jHl9IEOA8oGN4u0yeLnbZVOLcpGBGxA6eMH2aC0QCSyNR8eso6C6L3HrG9",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCwaed1mg01ibcIsYzG_DGMkVJ-E8dmXbfKuoAJd4x9nHfVB2WJAi1TLJXpvYvPRO8Kda181_CC_lf5iqzBtRcgWl8WzzmjLsl3ktxHKMGiNPwOlYgj76PGnkri4QFquQe6fqyN3wF2qvLDHpSalkxe9jyRPyeBeY585rPst1R_cO2kgrPXktqZAPVyR7hyXazj_BHAcIuV9KiiFDkY11Hk6N_HSgYhpQtXPuyrXENB",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCbyRWFHVb4wNCMt4EfAIJ2EWnFByLxsepWuZ8LEL5ae16YhTSxkLc4wVAf6ZzsxQMIiTrwesMHSnkpPIDkry42dEBpIiAtwP_z5_-huViJJT3PB-C6BqHSMGmdRdSotR355Igja8j45GrK-UvbtEWwwVq3XfLwYQTMRLmNQI4O_LajSmC1d3JuVy9MVQJpxGPnozotbfJWK6SpJqGHkDC3azshMkgvRMwd3eQMwwpv"
        ]),
        "specifications": json.dumps({
            "Closure": "Bespoke 24K Gold Clasp & Dual Heavy-duty Zippers",
            "Compartments": "6 Adjustable Velvet Dividers + 5 Cosmetic Brush Slots",
            "Strap": "Detachable Calf-leather Shoulder Strap with Chain Link",
            "Weight": "1.15 kg",
            "Warranty": "1-Year Atelier Craftsmanship Warranty"
        })
    },
    {
        "id": 2,
        "slug": "aria-quilted-mini-sling",
        "name": "Aria Quilted Mini Sling",
        "category": "Sling & Crossbody",
        "category_slug": "sling",
        "price": 2299.0,
        "original_price": 3199.0,
        "discount_percent": 28,
        "badge": "New",
        "rating": 4.8,
        "reviews_count": 64,
        "edition_tag": "Festive Atelier Collection",
        "short_description": "Chic chevron-quilted petite vanity sling bag with jewelry gold chain strap and twist turnlock fastener.",
        "description": "Embodying poise and evening romance, the Aria Quilted Mini Sling holds your phone, compact mirror, lip glosses, and heirloom cardholder in structured grace. The diamond-quilted lambskin finish catches warm sunset light gracefully.",
        "material": "Diamond-quilted Vegan Lambskin",
        "lining": "Blush microfiber suede",
        "hardware": "Polished Champagne Gold Turnlock & Interwoven Chain Strap",
        "dimensions": "20cm (L) x 8cm (W) x 14cm (H)",
        "provenance": "Handmade in Agra Atelier",
        "stock_quantity": 28,
        "is_featured": 1,
        "is_bestseller": 0,
        "is_new": 1,
        "colors": json.dumps([
            {"name": "Blush Pink", "hex": "#FFB2BA", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCAEz7ImXVeeAHC6s_EIipXh0nACpAjoL9F4Y8B2YmTcM8QY2ztyWoorxlDyyquqNqJUNHh1C1UwMhG4jmyFChSV8E_-0iTfGoUm4qMj6coEtsPYCcEK8rtxdofQ_GFpQFLH3HgEp7m8WAIHCh28cX_mnNOoVdqoeGsP2HNb3iw4KS_7e8cH7SjgwpJvIhoBXyaX37cRWeNt8BPYGi85YQf_psX6gmtHg_o8UNbG5_9"},
            {"name": "Champagne Pearl", "hex": "#E9C176", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuDOiuHXLOAtmRiGfIhqF0fWnyHCZRTFg7Q9e26hCCYGeWSQafYLDuFnZMkuPXsyJgDz47X-BafVf49BWCea3Rnx-gHlnQedZ_Jl9ZEVxVJz6Ac7NNxDhoqkZo-8GwRGF9lIvjRTZSgZnmL8GELyi2MTkMYumUdfB1H7D03GAHw5WUrXCgKh2Oq2GQMgL5gd19F1kEDmpRrlwdadCO4IkkQNZzzZICsVj7CyJTbJUjmi"}
        ]),
        "images": json.dumps([
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCAEz7ImXVeeAHC6s_EIipXh0nACpAjoL9F4Y8B2YmTcM8QY2ztyWoorxlDyyquqNqJUNHh1C1UwMhG4jmyFChSV8E_-0iTfGoUm4qMj6coEtsPYCcEK8rtxdofQ_GFpQFLH3HgEp7m8WAIHCh28cX_mnNOoVdqoeGsP2HNb3iw4KS_7e8cH7SjgwpJvIhoBXyaX37cRWeNt8BPYGi85YQf_psX6gmtHg_o8UNbG5_9",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuDOiuHXLOAtmRiGfIhqF0fWnyHCZRTFg7Q9e26hCCYGeWSQafYLDuFnZMkuPXsyJgDz47X-BafVf49BWCea3Rnx-gHlnQedZ_Jl9ZEVxVJz6Ac7NNxDhoqkZo-8GwRGF9lIvjRTZSgZnmL8GELyi2MTkMYumUdfB1H7D03GAHw5WUrXCgKh2Oq2GQMgL5gd19F1kEDmpRrlwdadCO4IkkQNZzzZICsVj7CyJTbJUjmi",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuDiCoaRUD8B7RFV3SpT6S68RoZoTuKD9SNZalt1Du3GBIBmAkwMjt1IftWOc9i9H0EqFzFMUKVvaoJedk4oqi6Bme5ydXd3Fb98BJnDoqpsO4Mx8NHz87DHoilsMC1es_EAiVN_eGENIpEqdFYf4L1kpjpVS5Y_1HGbl2J7w6Na7T_DuEhXxjHI_EscwjBk0hsq4szd9zlrBtMtXfp0nS5iVjmZ74ZO0hOsoGvvrCpA"
        ]),
        "specifications": json.dumps({
            "Closure": "Turnlock with Safety Clasp",
            "Compartments": "Main Chamber + Internal Card Pocket",
            "Strap": "Interlaced Gold Chain with Leather Shoulder Guard",
            "Weight": "480g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 3,
        "slug": "celeste-dual-compartment-case",
        "name": "Celeste Dual Compartment",
        "category": "Compartment Organisers",
        "category_slug": "organisers",
        "price": 1899.0,
        "original_price": 2499.0,
        "discount_percent": 24,
        "badge": "Popular",
        "rating": 4.7,
        "reviews_count": 92,
        "edition_tag": "Voyager Organisers",
        "short_description": "Two-tiered satin and textured leather cosmetic vanity case with dual metallic zippers and brush organizers.",
        "description": "Double the utility with immaculate separation: upper tiered section holds brushes, eye palettes, and tools in transparent protected slots, while the deep lower deck accommodates bottles, creams, and perfume flacons.",
        "material": "Structured Champagne Satin & Pebbled Vegan Leather",
        "lining": "Waterproof stain-resistant satin lining",
        "hardware": "Dual Smooth Glide Rose-Gold Zippers",
        "dimensions": "24cm (L) x 16cm (W) x 18cm (H)",
        "provenance": "Handcrafted in Kolkata Atelier",
        "stock_quantity": 35,
        "is_featured": 1,
        "is_bestseller": 0,
        "is_new": 0,
        "colors": json.dumps([
            {"name": "Champagne", "hex": "#E9C176", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuB5mWXUlsAHPn_j4jYtly6KzLXwi9MST_Z3tZrywByA21VcCaJf2QLZr9ifQEIJ3TAPTVx5dKa0uAsDm0CsBmfD-H1trDW1gytAWcxTLBxkUgXgmWqrU_vxECV6K4fJ_ofGGjZrkHVymWZPmaU0TQfxLYLocu4tdepdGV56PPSNsbvQXMLIYMlRE2BQ5s7PK1f2yyABnfn9zfjX5tFTgbTXPXzeuoTrws8XOOD347PU"},
            {"name": "Emerald Noir", "hex": "#1C1B1B", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuA0HNS1WpuRHOe6E6-DTPXcH10qDgZ_sqwyQZgdrG5u9RE6l_l7A-XKhcbB7WwXdJwdMqF19R59GeG53cYRgMYSI8LoRjQ9BkXiQpXLpJo_ogWRd0LGfvjetrvm4qUT8be1-T5U1ZyYc18VHiCqV-w-GHQ29P7M8mjXz3cDF3zcVS_C5zFvA7DzLrr_ULvo36exNy3fgAflIlAfpBFQSfirVdcXVFyqaobhL9zQkaW4"}
        ]),
        "images": json.dumps([
            "https://lh3.googleusercontent.com/aida-public/AB6AXuB5mWXUlsAHPn_j4jYtly6KzLXwi9MST_Z3tZrywByA21VcCaJf2QLZr9ifQEIJ3TAPTVx5dKa0uAsDm0CsBmfD-H1trDW1gytAWcxTLBxkUgXgmWqrU_vxECV6K4fJ_ofGGjZrkHVymWZPmaU0TQfxLYLocu4tdepdGV56PPSNsbvQXMLIYMlRE2BQ5s7PK1f2yyABnfn9zfjX5tFTgbTXPXzeuoTrws8XOOD347PU",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuA0HNS1WpuRHOe6E6-DTPXcH10qDgZ_sqwyQZgdrG5u9RE6l_l7A-XKhcbB7WwXdJwdMqF19R59GeG53cYRgMYSI8LoRjQ9BkXiQpXLpJo_ogWRd0LGfvjetrvm4qUT8be1-T5U1ZyYc18VHiCqV-w-GHQ29P7M8mjXz3cDF3zcVS_C5zFvA7DzLrr_ULvo36exNy3fgAflIlAfpBFQSfirVdcXVFyqaobhL9zQkaW4"
        ]),
        "specifications": json.dumps({
            "Closure": "Dual 360-degree Heavy Duty Zips",
            "Compartments": "Top Tool Deck + Bottom Bottle Reservoir",
            "Handle": "Reinforced Padded Top Handle",
            "Weight": "620g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 4,
        "slug": "lumina-cylindrical-bag",
        "name": "Lumina Cylindrical Bag",
        "category": "Vanity Cases & Trunks",
        "category_slug": "vanity",
        "price": 2799.0,
        "original_price": 3899.0,
        "discount_percent": 28,
        "badge": "Iconic",
        "rating": 5.0,
        "reviews_count": 43,
        "edition_tag": "Sculptural Series",
        "short_description": "Unique architectural cylindrical vanity bag in ivory calfskin texture with gold zip-around top.",
        "description": "Standing as a miniature sculpture, the Lumina Cylindrical Bag reinvents vanity luggage. A circular zip lid unveils upright storage that keeps delicate serums and sprays upright during commutes and flights.",
        "material": "Smooth Full-Grain Calfskin Leatherette",
        "lining": "Warm sand microfiber velvet",
        "hardware": "Circumferential 24K Brushed Brass Zip & Base Studs",
        "dimensions": "16cm (Diameter) x 20cm (Height)",
        "provenance": "Handcrafted in Mumbai Studio",
        "stock_quantity": 22,
        "is_featured": 1,
        "is_bestseller": 0,
        "is_new": 1,
        "colors": json.dumps([
            {"name": "Ivory Off-White", "hex": "#F5F3F0", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuA_QLhwUh8MdZ_GRquXpq7yZvI_MoEtD4DJuTKgUsaVdrJ0hngfmr1dZYpY0zI0GDsIxHiNGvy2ILTMq5_u0ZdUmgAFzOFDEVzNS8yAzS9L60wQ5vGdWF8dGudR9mhYxxSs5fAEm6xtDzPVN18E58Z0CDtYYQStfUld5aqsw2MMfWkblatjBraqWQv5jwz4t--WRv44ZVBHL_vXAEE5SKgU2pfmT0WeJGyVWUUtavPa"},
            {"name": "Saddle Brown", "hex": "#7A3F47", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCbZ-sqQibIGVmS_IJYcvMXwa7sapTTarEOxwIam7KY0E-9mD6WYLmxzfOdMdJVqUJo6f3Vg1cdTFU6fOZ5-MkwMunkc_55FzW9xnYGGuaMiU83Uvz7wnfRjdtqvw94derwvcU5UnblDEkgSrTtsfQ7P2zp9142LtehQuyIqUczxCVMGL46RHqOzVxrv0xBmNoQ7zjkm7QeLo4SOuNh3cpZgJDHPE2codO5rxOQXpaB"}
        ]),
        "images": json.dumps([
            "https://lh3.googleusercontent.com/aida-public/AB6AXuA_QLhwUh8MdZ_GRquXpq7yZvI_MoEtD4DJuTKgUsaVdrJ0hngfmr1dZYpY0zI0GDsIxHiNGvy2ILTMq5_u0ZdUmgAFzOFDEVzNS8yAzS9L60wQ5vGdWF8dGudR9mhYxxSs5fAEm6xtDzPVN18E58Z0CDtYYQStfUld5aqsw2MMfWkblatjBraqWQv5jwz4t--WRv44ZVBHL_vXAEE5SKgU2pfmT0WeJGyVWUUtavPa",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCcXchh7qMREiswUXgwRUOQ-1HMcZop_teYQyMjERrT_CNKQgbKdp6dJa6K6g2cfEdP9CAORNEkCpOX_Yyes05wZjl287RpU8z1te64UIl2Z8RKQ6BJow45YwthHOiraKeu5c8mOmoAjXdR31yLpU9oSppqPfWWV_WdD-gyUmdh-iBGy2S8GfDY70i7gIh8bzp964iiIfpeOCOrk-deq3U5vbJH48C9yd4ZPbmCSbE2"
        ]),
        "specifications": json.dumps({
            "Closure": "Top Circular Zip Canopy",
            "Base": "4 Protective Brass Stud Feet",
            "Strap": "Adjustable Crossbody Strap + Rigid Top Arch Handle",
            "Weight": "510g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 5,
        "slug": "velvet-horizon-trunk",
        "name": "Velvet Horizon Trunk",
        "category": "Vanity Cases & Trunks",
        "category_slug": "vanity",
        "price": 1499.0,
        "original_price": 1999.0,
        "discount_percent": 25,
        "badge": "Artisan Choice",
        "rating": 4.6,
        "reviews_count": 78,
        "edition_tag": "Trousseau Classic",
        "short_description": "Deep ruby crimson plush velvet portable cosmetics chest with gold lock and vanity mirror lid.",
        "description": "Richly evocative of heritage Indian royal courts, the Velvet Horizon Trunk is upholstered in tactile crimson silk velvet. Inside, a beveled glass vanity mirror and removable velvet ring rolls ensure seamless bridal touch-ups.",
        "material": "Plush Jewel-toned Velvet with Leather Piping",
        "lining": "Tonal crimson quilted velvet",
        "hardware": "Burnished Gold Clasp with Integrated Mirror Hinges",
        "dimensions": "22cm (L) x 15cm (W) x 12cm (H)",
        "provenance": "Handcrafted in Jaipur Atelier",
        "stock_quantity": 50,
        "is_featured": 0,
        "is_bestseller": 0,
        "is_new": 0,
        "colors": json.dumps([
            {"name": "Ruby Velvet", "hex": "#8A4C54", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuBVZsiPm6p-SqtkYy9bhka-WWCFTIEh_lmKKp_YuLi4opgtTgXsGfjNZG2eDtFtrJ7c7OLa37U_p1LtMdjWDtJQFl5TDHgoeswEVPg9MJQkOj3uTUNhqyERTp6CfsUhNeDYSq20aDLsKyRF9hY4LN520hAc9iOKP91GUpxvAiSLz0i9gXpJT-G24BfWGvg8EuAewMu3le9yZDMZmUickMdAQYIM0APU9C5FCJthfpuW"},
            {"name": "Dusty Rose", "hex": "#FDAFB7", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuBOKQs8mxbhaO7SGm4WfOOZL6WP6y3QVatlTxYbQk3qDTZvWGlkJ-tpmvSUDmclcYa9yE1bCKcSiZ725aYAtcIaFS38QbrLbieRFZcbuzEYUWai77jZOdubLjMvE-yElhAmvo3rdXH4cL02o2Zt-I9StoTUYwmc6wSvdjyj4cJOEjO5h_YGJEOUk2vIeUcHefmOwje1l8_XLd9fQuXGthjLmgbNK3G-DsShPRtPGNZd"}
        ]),
        "images": json.dumps([
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBVZsiPm6p-SqtkYy9bhka-WWCFTIEh_lmKKp_YuLi4opgtTgXsGfjNZG2eDtFtrJ7c7OLa37U_p1LtMdjWDtJQFl5TDHgoeswEVPg9MJQkOj3uTUNhqyERTp6CfsUhNeDYSq20aDLsKyRF9hY4LN520hAc9iOKP91GUpxvAiSLz0i9gXpJT-G24BfWGvg8EuAewMu3le9yZDMZmUickMdAQYIM0APU9C5FCJthfpuW",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBOKQs8mxbhaO7SGm4WfOOZL6WP6y3QVatlTxYbQk3qDTZvWGlkJ-tpmvSUDmclcYa9yE1bCKcSiZ725aYAtcIaFS38QbrLbieRFZcbuzEYUWai77jZOdubLjMvE-yElhAmvo3rdXH4cL02o2Zt-I9StoTUYwmc6wSvdjyj4cJOEjO5h_YGJEOUk2vIeUcHefmOwje1l8_XLd9fQuXGthjLmgbNK3G-DsShPRtPGNZd"
        ]),
        "specifications": json.dumps({
            "Mirror": "Integrated Beveled Glass Vanity Mirror",
            "Closure": "Faceted Gold Snap Clasp",
            "Compartments": "Modular Velvet Dividers + Ring Cushions",
            "Weight": "420g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 6,
        "slug": "serena-organiser-tote",
        "name": "Serena Organiser Tote",
        "category": "Artisanal Totes",
        "category_slug": "totes",
        "price": 2999.0,
        "original_price": 4299.0,
        "discount_percent": 30,
        "badge": "Bestseller",
        "rating": 4.9,
        "reviews_count": 115,
        "edition_tag": "Urban Atelier",
        "short_description": "Sophisticated biscuit beige canvas and rich leather trimmed multi-pocket organizer tote with internal vanity sections.",
        "description": "Tailored for dynamic women whose days glide effortlessly from boardrooms to soirées. Features an internal insulated bottle caddy, a padded 13.5\" laptop cradle, and a dedicated zippered vanity organizer that unzips independently.",
        "material": "Water-repellent Heavyweight Organic Canvas & Full-grain Tan Leather",
        "lining": "Stain-resistant sand twill",
        "hardware": "Brushed Champagne Gold D-rings & Studs",
        "dimensions": "38cm (L) x 16cm (W) x 29cm (H)",
        "provenance": "Handcrafted in New Delhi Atelier",
        "stock_quantity": 38,
        "is_featured": 1,
        "is_bestseller": 1,
        "is_new": 0,
        "colors": json.dumps([
            {"name": "Biscuit Beige & Tan", "hex": "#EAE8E5", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCDKqvMpyYptxom7SNDzNlZFW221VnFRPn_ER-df7Ap-cXB_NQNLwXH9v-lzqsQuSbu11cYqNxmT-G2gVuyAr2F0j0tc1gm1m2wF3FWOoBt7LmLcUHIm6oaFIt-Nm7ArpAOODkY4nndseBvgkM3OP13q_6wqbsE9SHEBRB6-qV6Kqjrv-M-f2EXHzpUuPLDQVxMNS-6txtv-zKj_P88wIXYgnRC2O-YDx5aahFD0-5w"},
            {"name": "Midnight Black", "hex": "#1C1B1B", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCbZ-sqQibIGVmS_IJYcvMXwa7sapTTarEOxwIam7KY0E-9mD6WYLmxzfOdMdJVqUJo6f3Vg1cdTFU6fOZ5-MkwMunkc_55FzW9xnYGGuaMiU83Uvz7wnfRjdtqvw94derwvcU5UnblDEkgSrTtsfQ7P2zp9142LtehQuyIqUczxCVMGL46RHqOzVxrv0xBmNoQ7zjkm7QeLo4SOuNh3cpZgJDHPE2codO5rxOQXpaB"}
        ]),
        "images": json.dumps([
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCDKqvMpyYptxom7SNDzNlZFW221VnFRPn_ER-df7Ap-cXB_NQNLwXH9v-lzqsQuSbu11cYqNxmT-G2gVuyAr2F0j0tc1gm1m2wF3FWOoBt7LmLcUHIm6oaFIt-Nm7ArpAOODkY4nndseBvgkM3OP13q_6wqbsE9SHEBRB6-qV6Kqjrv-M-f2EXHzpUuPLDQVxMNS-6txtv-zKj_P88wIXYgnRC2O-YDx5aahFD0-5w",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCbZ-sqQibIGVmS_IJYcvMXwa7sapTTarEOxwIam7KY0E-9mD6WYLmxzfOdMdJVqUJo6f3Vg1cdTFU6fOZ5-MkwMunkc_55FzW9xnYGGuaMiU83Uvz7wnfRjdtqvw94derwvcU5UnblDEkgSrTtsfQ7P2zp9142LtehQuyIqUczxCVMGL46RHqOzVxrv0xBmNoQ7zjkm7QeLo4SOuNh3cpZgJDHPE2codO5rxOQXpaB"
        ]),
        "specifications": json.dumps({
            "Laptop Sleeve": "Padded chamber fits up to 14\" MacBook Pro",
            "Vanity Pod": "Detachable internal zip pouch for cosmetics",
            "Drop Handles": "26cm handle drop for comfortable shoulder carry",
            "Weight": "820g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 7,
        "slug": "petite-atelier-organizer-pouch",
        "name": "Petite Atelier Organizer Pouch",
        "category": "Compartment Organisers",
        "category_slug": "organisers",
        "price": 1719.0,
        "original_price": 2299.0,
        "discount_percent": 25,
        "badge": "Essential",
        "rating": 4.8,
        "reviews_count": 52,
        "edition_tag": "Daily Luxuries",
        "short_description": "Artisanal saffiano leather cosmetics clutch bag with rose gold metallic zipper detail.",
        "description": "The quintessential handbag companion. Slip it into any tote or carry it solo as an understated minimalist clutch. Water-resistant interior cleans with a single gentle wipe.",
        "material": "Cross-grain Saffiano Vegan Leather",
        "lining": "Easy-clean champagne twill",
        "hardware": "Jeweled Rose Gold Zip Puller",
        "dimensions": "21cm (L) x 6cm (W) x 13cm (H)",
        "provenance": "Handcrafted in Agra, India",
        "stock_quantity": 60,
        "is_featured": 0,
        "is_bestseller": 0,
        "is_new": 0,
        "colors": json.dumps([
            {"name": "Rose Blush", "hex": "#FDAFB7", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuAIC_nEDUhtBmrtFnWgr-pBFPYe1bnWR2XT8S2xU7oqYQVOlgZS1UKKztEAx_MSbwPIbM0MxZnooVP8oEVTclJ1doDSHfJZg1Aw9tcGzlyj431xcjN1L6t_4KOCy0qAgdH_4JH3fVrtRBQTA09RLBwJa6ejtSBTPLgzmf4xO7K4wNoxZ4axJfo6VlJtAHVllPpLBsyuZTVKMjgZ419hftgD7a9rMlXXf3boDPZwFTIe"},
            {"name": "Champagne Dune", "hex": "#E9C176", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCHoIz511UdCvPAYuysvWPFSjuI0lTgwf_38tipAg2_ojXOsM2jFUXXjEfLC3gH6e2RGNTi_vIJlpWThb5Dy8zyPO09-Hc1qPv6VLphbhHJPVakmTk-JVyZkA1iGgBF3lbvH3woeWx9KUYiwmfLgFBnpIawEcUc4tbXBBXy7Pa-I2EKFjZvLJr8L21vWRhZuDVQ2lvfql9WeT61BlOkIeS3eSsFbd9a8sK9wwOrGMzK"}
        ]),
        "images": json.dumps([
            "https://lh3.googleusercontent.com/aida-public/AB6AXuAIC_nEDUhtBmrtFnWgr-pBFPYe1bnWR2XT8S2xU7oqYQVOlgZS1UKKztEAx_MSbwPIbM0MxZnooVP8oEVTclJ1doDSHfJZg1Aw9tcGzlyj431xcjN1L6t_4KOCy0qAgdH_4JH3fVrtRBQTA09RLBwJa6ejtSBTPLgzmf4xO7K4wNoxZ4axJfo6VlJtAHVllPpLBsyuZTVKMjgZ419hftgD7a9rMlXXf3boDPZwFTIe",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCHoIz511UdCvPAYuysvWPFSjuI0lTgwf_38tipAg2_ojXOsM2jFUXXjEfLC3gH6e2RGNTi_vIJlpWThb5Dy8zyPO09-Hc1qPv6VLphbhHJPVakmTk-JVyZkA1iGgBF3lbvH3woeWx9KUYiwmfLgFBnpIawEcUc4tbXBBXy7Pa-I2EKFjZvLJr8L21vWRhZuDVQ2lvfql9WeT61BlOkIeS3eSsFbd9a8sK9wwOrGMzK"
        ]),
        "specifications": json.dumps({
            "Closure": "Heavy Duty Metallic Top Zip",
            "Interior": "3 Card Slots + 2 Elasticized Lipstick Rings",
            "Weight": "210g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 8,
        "slug": "chloe-petite-jewellery-case",
        "name": "Chloe Petite Jewellery Pod",
        "category": "Jewellery Boxes",
        "category_slug": "jewelry",
        "price": 1299.0,
        "original_price": 1799.0,
        "discount_percent": 28,
        "badge": "Gifting Favorite",
        "rating": 4.9,
        "reviews_count": 87,
        "edition_tag": "Heirloom Gifting",
        "short_description": "Petite compact travel jewelry case wrapped in soft powder pink leather open to display rings, bangles, and necklaces.",
        "description": "Never tangle another chain on your travels. The Chloe Petite Jewellery Pod safely harbors your precious earrings, necklaces, rings, and heirloom bangles on cushioned micro-velvet pillows.",
        "material": "Powder Pink Grain Leatherette",
        "lining": "Anti-tarnish microfiber velvet",
        "hardware": "Brushed Gold Zip Lock",
        "dimensions": "12cm (L) x 12cm (W) x 6cm (H)",
        "provenance": "Handcrafted in Jaipur Atelier",
        "stock_quantity": 45,
        "is_featured": 0,
        "is_bestseller": 0,
        "is_new": 1,
        "colors": json.dumps([
            {"name": "Powder Pink", "hex": "#FFD9DC", "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuBOKQs8mxbhaO7SGm4WfOOZL6WP6y3QVatlTxYbQk3qDTZvWGlkJ-tpmvSUDmclcYa9yE1bCKcSiZ725aYAtcIaFS38QbrLbieRFZcbuzEYUWai77jZOdubLjMvE-yElhAmvo3rdXH4cL02o2Zt-I9StoTUYwmc6wSvdjyj4cJOEjO5h_YGJEOUk2vIeUcHefmOwje1l8_XLd9fQuXGthjLmgbNK3G-DsShPRtPGNZd"}
        ]),
        "images": json.dumps([
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBOKQs8mxbhaO7SGm4WfOOZL6WP6y3QVatlTxYbQk3qDTZvWGlkJ-tpmvSUDmclcYa9yE1bCKcSiZ725aYAtcIaFS38QbrLbieRFZcbuzEYUWai77jZOdubLjMvE-yElhAmvo3rdXH4cL02o2Zt-I9StoTUYwmc6wSvdjyj4cJOEjO5h_YGJEOUk2vIeUcHefmOwje1l8_XLd9fQuXGthjLmgbNK3G-DsShPRtPGNZd"
        ]),
        "specifications": json.dumps({
            "Rings": "6 Cushioned Ring Rows",
            "Necklaces": "4 Tangle-free Hooks with Elastic Pouch",
            "Weight": "190g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 9,
        "slug": "the-jackie-crescent-hobo",
        "name": "The Jackie Crescent Hobo",
        "category": "Sling & Crossbody",
        "category_slug": "sling",
        "price": 4499.0,
        "original_price": 6499.0,
        "discount_percent": 30,
        "badge": "Iconic Silhouette",
        "rating": 4.9,
        "reviews_count": 84,
        "edition_tag": "Heritage 1961 Archive",
        "short_description": "Archival curved crescent shoulder hobo bag with gold piston push-lock closure and dual strap versatility.",
        "description": "Inspired by the jet-set era of the early 1960s, The Jackie Crescent Hobo captures timeless Italian allure with refined Indian artisanal craftsmanship. Defined by its curved half-moon silhouette and gold piston push-lock, this bag effortlessly transitions from daytime shoulder carry to an evening crossbody with its detachable extender strap.",
        "material": "Full-Grain Italian Calfskin Leatherette",
        "lining": "Blush microfiber suede with interior zip pocket",
        "hardware": "24K Gold Piston Lock & Engraved Swivel Hooks",
        "dimensions": "27.5cm (L) x 19cm (H) x 4.5cm (W)",
        "provenance": "Handcrafted in Florence & Jaipur Atelier",
        "stock_quantity": 30,
        "is_featured": 1,
        "is_bestseller": 1,
        "is_new": 0,
        "colors": json.dumps([
            {"name": "Emerald Green", "hex": "#1E4D3B", "image": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=800&q=80"},
            {"name": "Noir Black", "hex": "#1A1A1A", "image": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80"}
        ]),
        "images": json.dumps([
            "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80"
        ]),
        "specifications": json.dumps({
            "Closure": "Piston Push-Lock Clasp in 24K Brushed Brass",
            "Straps": "Fixed Leather Shoulder Handle + Detachable Crossbody Extender",
            "Pockets": "1 Interior Zip Chamber + 1 Open Card Slot",
            "Weight": "490g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 10,
        "slug": "the-horsebit-1955-flap-bag",
        "name": "The Horsebit 1955 Flap Bag",
        "category": "Sling & Crossbody",
        "category_slug": "sling",
        "price": 4899.0,
        "original_price": 6999.0,
        "discount_percent": 30,
        "badge": "Bestseller",
        "rating": 5.0,
        "reviews_count": 96,
        "edition_tag": "Equestrian Heritage Series",
        "short_description": "Timeless flap shoulder bag centered by the iconic double-ring and bar equestrian hardware.",
        "description": "Embodying equestrian elegance, The Horsebit 1955 Flap Bag celebrates neo-vintage proportions and structured symmetry. Handcrafted with rich vintage monogram jacquard and vegetable-tanned leather trim, it features the emblematic gilded equestrian bit across the front flap with three interior compartments.",
        "material": "Archival Monogram Jacquard & Saddle Tan Leather Trim",
        "lining": "Cotton linen lining with dual accordion partitions",
        "hardware": "Polished 24K Gold Equestrian Double Ring & Bar Clasp",
        "dimensions": "25cm (L) x 18cm (H) x 8cm (W)",
        "provenance": "Handcrafted in New Delhi Atelier",
        "stock_quantity": 25,
        "is_featured": 1,
        "is_bestseller": 1,
        "is_new": 1,
        "colors": json.dumps([
            {"name": "Saddle Brown & Monogram", "hex": "#7C4329", "image": "https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?auto=format&fit=crop&w=800&q=80"}
        ]),
        "images": json.dumps([
            "https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?auto=format&fit=crop&w=800&q=80"
        ]),
        "specifications": json.dumps({
            "Closure": "Front Flap with Concealed Magnetic Snap & Horsebit Hardware",
            "Compartments": "Three Accordion Sections + 1 Interior Zip Pocket",
            "Strap": "Adjustable Leather Shoulder Strap with Gold Snap Buttons (25-45cm drop)",
            "Weight": "650g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 11,
        "slug": "the-dionysus-spur-chain-bag",
        "name": "The Dionysus Spur Chain Bag",
        "category": "Sling & Crossbody",
        "category_slug": "sling",
        "price": 5299.0,
        "original_price": 7499.0,
        "discount_percent": 29,
        "badge": "New Arrival",
        "rating": 4.9,
        "reviews_count": 48,
        "edition_tag": "Mythos Collection",
        "short_description": "Sculpted structured flap bag adorned with a dual tiger-head spur buckle and sliding chain.",
        "description": "Referencing ancient mythology and timeless baroque flair, The Dionysus Spur Chain Bag features a unique textured double tiger-head spur closure. Crafted with structured coated canvas and plush suede side bellows, the sliding chain strap can be worn doubled over the shoulder or extended as a cross-body.",
        "material": "Durable Coated Canvas with Soft Taupe Suede Sides",
        "lining": "Natural suede microfiber with center zippered divider",
        "hardware": "Antiqued Silver-Tone Tiger Head Horseshoe Clasp with Pin Closure",
        "dimensions": "28cm (L) x 17cm (H) x 9cm (W)",
        "provenance": "Handcrafted in Jaipur Atelier",
        "stock_quantity": 20,
        "is_featured": 1,
        "is_bestseller": 0,
        "is_new": 1,
        "colors": json.dumps([
            {"name": "Taupe & Canvas", "hex": "#8C7D70", "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=800&q=80"}
        ]),
        "images": json.dumps([
            "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=800&q=80"
        ]),
        "specifications": json.dumps({
            "Closure": "Pin Closure with Side Release and Tiger Head Spur",
            "Chain": "Sliding Cut-Link Antiqued Silver Chain (Drop 38cm or 22cm doubled)",
            "Compartments": "Dual Main Compartments + Center Zippered Pocket",
            "Weight": "720g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 12,
        "slug": "the-bamboo-1947-top-handle",
        "name": "The Bamboo 1947 Top Handle",
        "category": "Vanity Cases & Trunks",
        "category_slug": "vanity",
        "price": 5999.0,
        "original_price": 8999.0,
        "discount_percent": 33,
        "badge": "Artisan Masterpiece",
        "rating": 5.0,
        "reviews_count": 62,
        "edition_tag": "Patina & Craft 1947",
        "short_description": "Curved top-handle bag featuring flame-bent natural bamboo handle and turnlock clasp.",
        "description": "A triumph of artisanal post-war ingenuity, The Bamboo 1947 is crowned with a genuine fire-shaped cane bamboo curved handle and matching bamboo turnlock. Sculpted in supple grain calfskin with hand-lacquered edges, it is an enduring conversation piece that bridges heritage craft and modern luxury.",
        "material": "Hand-Burnished Smooth Calfskin Leatherette",
        "lining": "Cream nappa leatherette interior with cosmetic pocket",
        "hardware": "Flame-Bent Natural Bamboo Handle & Turnlock with Champagne Brass Fittings",
        "dimensions": "21cm (L) x 15cm (H) x 7cm (W)",
        "provenance": "Artisan Hand-shaped in Bengaluru Atelier",
        "stock_quantity": 18,
        "is_featured": 1,
        "is_bestseller": 0,
        "is_new": 1,
        "colors": json.dumps([
            {"name": "Cognac Tan", "hex": "#9E5B32", "image": "https://images.unsplash.com/photo-1575032617751-6ddec2089882?auto=format&fit=crop&w=800&q=80"}
        ]),
        "images": json.dumps([
            "https://images.unsplash.com/photo-1575032617751-6ddec2089882?auto=format&fit=crop&w=800&q=80"
        ]),
        "specifications": json.dumps({
            "Handle": "Natural Cane Bamboo (Each piece holds unique grain and curvature)",
            "Strap": "Includes both a Tonal Leather Strap and an Embroidered Web Webbing Strap",
            "Mirror": "Includes removable mini vanity mirror in leather sleeve",
            "Weight": "540g",
            "Warranty": "2-Year Master Craft Warranty"
        })
    },
    {
        "id": 13,
        "slug": "the-marmont-chevron-matelasse",
        "name": "The Marmont Chevron Matelassé",
        "category": "Sling & Crossbody",
        "category_slug": "sling",
        "price": 3999.0,
        "original_price": 5499.0,
        "discount_percent": 27,
        "badge": "Most Loved",
        "rating": 4.9,
        "reviews_count": 112,
        "edition_tag": "Atelier Matelassé",
        "short_description": "Softly structured chevron-quilted shoulder bag with heart motif stitching and antique gold monogram clasp.",
        "description": "The Marmont Chevron Matelassé is instantly recognized by its distinctive chevron wave quilting with a stitched emblem on the reverse. Fitted with a sliding brass chain and leather shoulder guard, the soft shape and spring-closure flap open to a microfiber interior designed for effortless daily elegance.",
        "material": "Ultra-Soft Matelassé Chevron Calfskin Leatherette",
        "lining": "Microfiber with a suede-like finish",
        "hardware": "Antiqued Champagne Gold Interlocking Clasp and Curb Chain",
        "dimensions": "26cm (L) x 15cm (H) x 7cm (W)",
        "provenance": "Handcrafted in Mumbai Atelier",
        "stock_quantity": 35,
        "is_featured": 1,
        "is_bestseller": 1,
        "is_new": 0,
        "colors": json.dumps([
            {"name": "Dusty Rose", "hex": "#D98988", "image": "https://images.unsplash.com/photo-1591561954557-26941169b49e?auto=format&fit=crop&w=800&q=80"}
        ]),
        "images": json.dumps([
            "https://images.unsplash.com/photo-1591561954557-26941169b49e?auto=format&fit=crop&w=800&q=80"
        ]),
        "specifications": json.dumps({
            "Closure": "Spring Clasp Flap with Hidden Push-Release",
            "Chain": "Sliding Chain Strap (55cm drop as crossbody, 30cm drop as shoulder)",
            "Interior": "Internal Zippered Pocket & Phone Sleeve",
            "Weight": "590g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 14,
        "slug": "the-diana-bamboo-structured-tote",
        "name": "The Diana Bamboo Structured Tote",
        "category": "Artisanal Totes",
        "category_slug": "totes",
        "price": 5499.0,
        "original_price": 7999.0,
        "discount_percent": 31,
        "badge": "Royal Icon",
        "rating": 4.9,
        "reviews_count": 73,
        "edition_tag": "Princess Heritage Edition",
        "short_description": "Structured medium luxury leather tote with curved bamboo top handles and vibrant handle belt bands.",
        "description": "Favored by royalty and fashion icons worldwide, The Diana Tote balances classic rectangular structure with organic bamboo handles. Comes equipped with signature fluorescent leather handle bands—a playful tribute to the functional bands once used to maintain handle curvature.",
        "material": "Rich Fine-Grain Pebbled Vegan Leather",
        "lining": "Microfiber suede lining in warm oatmeal",
        "hardware": "Flame-Treated Natural Bamboo Handles with Gilded Hardware & Neon Straps",
        "dimensions": "35cm (L) x 28cm (H) x 14cm (W)",
        "provenance": "Handmade in Kolkata Atelier",
        "stock_quantity": 22,
        "is_featured": 1,
        "is_bestseller": 1,
        "is_new": 1,
        "colors": json.dumps([
            {"name": "Warm Caramel & Emerald Band", "hex": "#A0633B", "image": "https://images.unsplash.com/photo-1594223274512-ad4803739b7c?auto=format&fit=crop&w=800&q=80"}
        ]),
        "images": json.dumps([
            "https://images.unsplash.com/photo-1594223274512-ad4803739b7c?auto=format&fit=crop&w=800&q=80"
        ]),
        "specifications": json.dumps({
            "Handles": "Twin Bamboo Handles (11cm drop) + Neon Leather Handle Shapers",
            "Shoulder Strap": "Detachable and Adjustable Leather Shoulder Strap (50cm drop)",
            "Compartments": "Double Compartment with Center Partition Pocket",
            "Weight": "910g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 15,
        "slug": "the-ophidia-heritage-beauty-trunk",
        "name": "The Ophidia Heritage Beauty Trunk",
        "category": "Vanity Cases & Trunks",
        "category_slug": "vanity",
        "price": 4799.0,
        "original_price": 6499.0,
        "discount_percent": 26,
        "badge": "Voyage Classic",
        "rating": 4.8,
        "reviews_count": 59,
        "edition_tag": "Grand Tour 1930s",
        "short_description": "Signature trunk vanity case with green & red atelier webbing stripe and double-zip lid.",
        "description": "Recalling the romantic golden age of transatlantic rail and sea voyage, The Ophidia Heritage Beauty Trunk fuses archival heritage print with iconic two-tone red & green atelier ribbon webbing. Inside, a 360-degree vanity mirror and elasticized cosmetic flask holders keep your grooming essentials pristine.",
        "material": "Supreme Monogram Coated Canvas with Brown Leather Trim",
        "lining": "Water-resistant wipe-clean champagne satin",
        "hardware": "Double Directional 24K Brushed Gold Zippers & Atelier Medallion",
        "dimensions": "24cm (L) x 16cm (W) x 14cm (H)",
        "provenance": "Handcrafted in New Delhi Atelier",
        "stock_quantity": 28,
        "is_featured": 1,
        "is_bestseller": 0,
        "is_new": 0,
        "colors": json.dumps([
            {"name": "Heritage Monogram & Ribbon", "hex": "#5C4533", "image": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80"}
        ]),
        "images": json.dumps([
            "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80"
        ]),
        "specifications": json.dumps({
            "Lid": "Zip-Around Top Lid with Interior Elastic Pocket & Mirror",
            "Interior": "4 Elasticized Cosmetic Bottle Loops + Modular Velvet Section",
            "Strap": "Reinforced Top Arch Handle + Detachable Shoulder Strap",
            "Weight": "680g",
            "Warranty": "1-Year Atelier Warranty"
        })
    },
    {
        "id": 16,
        "slug": "the-padlock-key-lock-saddle-bag",
        "name": "The Padlock Key-Lock Saddle Bag",
        "category": "Sling & Crossbody",
        "category_slug": "sling",
        "price": 3799.0,
        "original_price": 5199.0,
        "discount_percent": 27,
        "badge": "Atelier Classic",
        "rating": 4.8,
        "reviews_count": 68,
        "edition_tag": "Vault Lock Edition",
        "short_description": "Structured saddle shoulder bag with archival padlock closure and enclosed leather key clochette.",
        "description": "Direct from the atelier archives, The Padlock Key-Lock Saddle Bag is defined by its architectural lock mechanism straight from travel trunk origins. The key is neatly encased in a detachable leather key bell clochette hanging from the strap.",
        "material": "Smooth Box Calfskin Leatherette & Monogram Coated Canvas",
        "lining": "Plush micro-velvet in almond beige",
        "hardware": "Polished Gold-Tone Key Lock Clasp with Working Key Clochette",
        "dimensions": "20.5cm (L) x 13cm (H) x 7.5cm (W)",
        "provenance": "Handcrafted in Agra Atelier",
        "stock_quantity": 32,
        "is_featured": 1,
        "is_bestseller": 0,
        "is_new": 1,
        "colors": json.dumps([
            {"name": "Black & Vintage Canvas", "hex": "#222222", "image": "https://images.unsplash.com/photo-1524498250077-390f9e378fc0?auto=format&fit=crop&w=800&q=80"}
        ]),
        "images": json.dumps([
            "https://images.unsplash.com/photo-1524498250077-390f9e378fc0?auto=format&fit=crop&w=800&q=80"
        ]),
        "specifications": json.dumps({
            "Lock": "Key Lock Closure with Sliding Lock Mechanism & Key Case",
            "Chain": "Sliding Gold Curb Chain (50cm drop crossbody, 28cm drop shoulder)",
            "Pockets": "1 Exterior Rear Slip Pocket + 1 Interior Slip Pocket",
            "Weight": "460g",
            "Warranty": "1-Year Atelier Warranty"
        })
    }
]

REVIEWS = [
    {
        "product_id": 1,
        "author": "Ananya Sharma",
        "location": "Bandra, Mumbai",
        "rating": 5,
        "title": "Pure Heirloom Quality!",
        "comment": "The Royale Trunk exceeded all expectations. The 24k brushed brass clasp has that satisfying, solid luxury weight. My entire wedding vanity setup looks ethereal with this case.",
        "verified": 1
    },
    {
        "product_id": 1,
        "author": "Pooja Singhania",
        "location": "Defence Colony, New Delhi",
        "rating": 5,
        "title": "Worth every single rupee",
        "comment": "The interior velvet lining is so soft and the partitions don't shift during travel. Received so many compliments at my cousin's destination wedding!",
        "verified": 1
    },
    {
        "product_id": 1,
        "author": "Meera Iyer",
        "location": "Indiranagar, Bengaluru",
        "rating": 4,
        "title": "Delivered in 2 days. Stunning craft.",
        "comment": "Pan-India express shipping was ultra-fast. Packaging was like unwrapping a luxury jewelry box. The rose gold shade is subtle, not garish.",
        "verified": 1
    },
    {
        "product_id": 2,
        "author": "Rhea Kapoor",
        "location": "Jubilee Hills, Hyderabad",
        "rating": 5,
        "title": "Chic & versatile for evening parties",
        "comment": "Fits my iPhone Pro Max, compact powder, and lipstick effortlessly. The woven gold chain doesn't pinch shoulders at all.",
        "verified": 1
    },
    {
        "product_id": 6,
        "author": "Sunita Verma",
        "location": "Vasant Kunj, New Delhi",
        "rating": 5,
        "title": "The ultimate workday commute tote",
        "comment": "The dedicated vanity zip compartment is a genius touch. My makeup stays separate from my laptop and paperwork.",
        "verified": 1
    },
    {
        "product_id": 9,
        "author": "Tara Aluwahlia",
        "location": "Colaba, Mumbai",
        "rating": 5,
        "title": "The archival hobo curve is iconic",
        "comment": "The Jackie crescent curve sits perfectly under my arm. The piston lock mechanism is heavy, authentic brass and gives that immediate heritage luxury impression.",
        "verified": 1
    },
    {
        "product_id": 10,
        "author": "Natasha Singhal",
        "location": "Golf Links, New Delhi",
        "rating": 5,
        "title": "Equestrian perfection & immaculate symmetry",
        "comment": "The Horsebit double-ring bar is dazzling. Three spacious partitions inside make it both a museum-grade collector piece and an effortless day bag.",
        "verified": 1
    },
    {
        "product_id": 11,
        "author": "Devika Nambiar",
        "location": "Kochi, Kerala",
        "rating": 5,
        "title": "The tiger spur clasp is pure art",
        "comment": "The double tiger-head spur buckle has astonishing dimensional detail. Sliding chain lets me wear it long across the chest or doubled for galas.",
        "verified": 1
    },
    {
        "product_id": 12,
        "author": "Kavita Sethi",
        "location": "Koramangala, Bengaluru",
        "rating": 5,
        "title": "The flame-bent bamboo handle is sublime",
        "comment": "Unbelievable craftsmanship. The genuine heat-shaped bamboo top handle and matching turnlock are heirloom tier. Everyone stops to ask where I acquired it.",
        "verified": 1
    },
    {
        "product_id": 13,
        "author": "Priyanka Roy",
        "location": "Alipore, Kolkata",
        "rating": 5,
        "title": "The softest chevron matelassé leather",
        "comment": "Sumptuously plush chevron quilting. Light as air yet holds my essentials with regal composure.",
        "verified": 1
    },
    {
        "product_id": 14,
        "author": "Shalini Mehra",
        "location": "Sector 15, Chandigarh",
        "rating": 5,
        "title": "Royal Diana vibes with modern panache",
        "comment": "The structured tote proportions paired with the organic bamboo arch handles and emerald bands are showstoppers. Exquisite stitching throughout.",
        "verified": 1
    },
    {
        "product_id": 15,
        "author": "Ayesha Farooqi",
        "location": "Banjara Hills, Hyderabad",
        "rating": 5,
        "title": "Vintage transatlantic vanity glamour",
        "comment": "The green and red webbing stripe against the heritage monogram canvas brings 1930s luxury voyage elegance to my dressing table.",
        "verified": 1
    },
    {
        "product_id": 16,
        "author": "Radhika Jaikishan",
        "location": "Malabar Hill, Mumbai",
        "rating": 5,
        "title": "Archival padlock click is so satisfying",
        "comment": "The key encased in the leather clochette bell actually works! Pure archival charm with modern everyday crossbody convenience.",
        "verified": 1
    }
]

COUPONS = [
    {
        "code": "EJITAS10",
        "discount_percent": 10.0,
        "discount_amount": 0.0,
        "min_order": 1499.0,
        "description": "10% off on your entire luxury order"
    },
    {
        "code": "WELCOME20",
        "discount_percent": 20.0,
        "discount_amount": 0.0,
        "min_order": 2499.0,
        "description": "20% off for first-time atelier connoisseurs"
    },
    {
        "code": "ATELIER500",
        "discount_percent": 0.0,
        "discount_amount": 500.0,
        "min_order": 3000.0,
        "description": "Flat ₹500 off on bridal vanity orders above ₹3,000"
    }
]

def seed_database():
    init_db()
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Upsert all products
        for p in PRODUCTS:
            cursor.execute("""
            INSERT INTO products (
                id, slug, name, category, category_slug, price, original_price, discount_percent,
                badge, rating, reviews_count, edition_tag, short_description, description,
                material, lining, hardware, dimensions, provenance, stock_quantity,
                is_featured, is_bestseller, is_new, colors, images, specifications
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                slug=excluded.slug,
                name=excluded.name,
                category=excluded.category,
                category_slug=excluded.category_slug,
                price=excluded.price,
                original_price=excluded.original_price,
                discount_percent=excluded.discount_percent,
                badge=excluded.badge,
                rating=excluded.rating,
                reviews_count=excluded.reviews_count,
                edition_tag=excluded.edition_tag,
                short_description=excluded.short_description,
                description=excluded.description,
                material=excluded.material,
                lining=excluded.lining,
                hardware=excluded.hardware,
                dimensions=excluded.dimensions,
                provenance=excluded.provenance,
                stock_quantity=excluded.stock_quantity,
                is_featured=excluded.is_featured,
                is_bestseller=excluded.is_bestseller,
                is_new=excluded.is_new,
                colors=excluded.colors,
                images=excluded.images,
                specifications=excluded.specifications
            """, (
                p["id"], p["slug"], p["name"], p["category"], p["category_slug"],
                p["price"], p["original_price"], p["discount_percent"], p["badge"],
                p["rating"], p["reviews_count"], p["edition_tag"], p["short_description"],
                p["description"], p["material"], p["lining"], p["hardware"],
                p["dimensions"], p["provenance"], p["stock_quantity"],
                p["is_featured"], p["is_bestseller"], p["is_new"],
                p["colors"], p["images"], p["specifications"]
            ))
        print(f"Upserted {len(PRODUCTS)} products.")
            
        # Seed Reviews
        for r in REVIEWS:
            cursor.execute("SELECT id FROM reviews WHERE product_id = ? AND author = ?", (r["product_id"], r["author"]))
            if not cursor.fetchone():
                cursor.execute("""
                INSERT INTO reviews (product_id, author, location, rating, title, comment, verified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (r["product_id"], r["author"], r["location"], r["rating"], r["title"], r["comment"], r["verified"]))
        print(f"Synced reviews.")

        # Seed Coupons
        for c in COUPONS:
            cursor.execute("SELECT code FROM coupons WHERE code = ?", (c["code"],))
            if not cursor.fetchone():
                cursor.execute("""
                INSERT INTO coupons (code, discount_percent, discount_amount, min_order, description)
                VALUES (?, ?, ?, ?, ?)
                """, (c["code"], c["discount_percent"], c["discount_amount"], c["min_order"], c["description"]))
        print(f"Synced coupons.")

if __name__ == "__main__":
    seed_database()
