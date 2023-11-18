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


# python3 main.py boldsnacks extract --option init 
#test_tag
# python3 main.py under_labz extract --option init
# python3 main.py max_titanium extract --option update_pages
# python3 main.py darkness extract --option update_products

# python3 main.py integralmedica dry --option init

marcas=("adaptogen" "atlhetica_nutrition" "black_skull" "boldsnacks" "dark_lab" "darkness" "dux_nutrition_lab" "growth_supplements" "integralmedica" "iridium_labs" "max_titanium" "new_millen" "nutrata" "probiotica" "under_labz")
for marca in "${marcas[@]}"
do
    python3 main.py "$marca" ingestion
done

# python3 main.py darkness ingestion