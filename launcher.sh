# extract init -> primeira execução ou recupreação
# extract update_products -> faz a extração de todos os produtos da pagina principal
# extract update_pages -> atualiza os produtos pela pagina do produto e atualiza o html armazenado
# extract test_tag -> testa se a extração funciona

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

# python3 main.py darkness extract --option init
# python3 main.py max_titanium extract --option test_tag
# python3 main.py darkness extract --option update_pages
# python3 main.py darkness extract --option update_products
python3 main.py darkness dry --option default
# python3 main.py darkness ingestion
# python3 main.py _set_ ingestion

# marcas=("adaptogen" "atlhetica_nutrition" "black_skull" "boldsnacks" "dark_lab" "darkness" "dux_nutrition_lab" "growth_supplements" "integralmedica" "iridium_labs" "max_titanium" "new_millen" "nutrata" "probiotica" "under_labz")
# for marca in "${marcas[@]}"
# do
#     python3 main.py "$marca" ingestion
# done
