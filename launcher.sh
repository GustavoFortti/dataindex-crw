# adaptogen
# atlhetica_nutrition
# black_skull
# boldsnacks
# dark_lab
# darkness
# dux_nutrition_lab 
# growth_supplements
# integralmedica 
# iridium_labs
# max_titanium 
# new_millen
# nutrata
# probiotica 
# under_labz

source ./.env/setup.sh


# python3 main.py probiotica extract --option init 
# python3 main.py dux_nutrition_lab extract --option test_tag
# python3 main.py darkness extract --option update_pages
python3 main.py darkness extract --option update_products

python3 main.py darkness dry --option init
python3 main.py darkness ingestion

# marcas=("adaptogen" "atlhetica_nutrition" "black_skull" "boldsnacks" "dark_lab" "darkness" "dux_nutrition_lab" "growth_supplements" "integralmedica" "iridium_labs" "max_titanium" "new_millen" "nutrata" "probiotica" "under_labz")
# for marca in "${marcas[@]}"
# do
#     python3 main.py "$marca" dry --option init
#     python3 main.py "$marca" ingestion
# done
