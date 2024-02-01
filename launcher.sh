export LOCAL=$(pwd)
source ./.env/setup.sh
bash ./.env/entrypoint.sh

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

# python3 main.py darkness extract --option init
# python3 main.py max_titanium extract --option test_tag
# python3 main.py darkness extract --option update_pages
# python3 main.py darkness extract --option update_products
# python3 main.py darkness dry --option default
# python3 main.py darkness ingestion
# python3 main.py _set_ ingestion

# marcas=("adaptogen" "atlhetica_nutrition" "black_skull" "boldsnacks" "dark_lab" "darkness" "dux_nutrition_lab" "growth_supplements" "integralmedica" "iridium_labs" "max_titanium" "new_millen" "nutrata" "probiotica" "under_labz")
# for marca in "${marcas[@]}"
# do
#     python3 main.py "$marca" extract --option init
# done
