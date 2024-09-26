from config.env import LOCAL
from lib.dataframe_functions import (filter_dataframe_for_columns,
                                     read_and_stack_csvs_dataframes)
from lib.elasticsearch.elasticsearch_functions import data_ingestion
from lib.elasticsearch.elasticsearch_index import INDEX_SUPPLEMENT_BRAZIL
from lib.set_functions import get_pages_with_status_true
from utils.log import message
from utils.wordlist import WORDLIST

CONF = {
    "name": "_set_carousel_",
    "data_path": f"{LOCAL}/data/supplement/brazil/_set_carousel_",
    "src_data_path": f"{LOCAL}/data/supplement/brazil",
    "pages_path": f"{LOCAL}/jobs/supplement/brazil/pages",
    "wordlist": WORDLIST["supplement"],
    "index_name": "",
    "index_type": INDEX_SUPPLEMENT_BRAZIL['type'],
}

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF.update(vars(args))

    job_type = CONF["job_type"]
    print(" - job_type: " + job_type)
    
    global WORDLIST
    WORDLIST = WORDLIST["supplement"]
    src_data_path = CONF["src_data_path"]

    pages_with_status_true = get_pages_with_status_true(CONF)
    df = read_and_stack_csvs_dataframes(src_data_path, pages_with_status_true, "origin_csl.csv")
    df = df.drop_duplicates(subset='ref').reset_index(drop=True)

    message("set whey")
    keywords = WORDLIST["whey"]["subject"]
    barrinha = WORDLIST["barrinha"]["subject"]
    alfajor = WORDLIST["alfajor"]["subject"]
    wafer = WORDLIST["wafer"]["subject"]
    blacklist = ["combo", "pack", "kit"] + barrinha + alfajor + wafer

    df_whey = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    df_whey = df_whey[df_whey['ref'].isin(["ef0c14a0", "2fb494c9", "9085321c", "16569443", "6b3d1d7c", "eb1210ea", "f2a24720", "d8dda1e7", "82b01c86", "b51c00a0", "fb0dc374", "77ad191e", "f0df6fa3", "775ecbf3", "68300995", "e03ef582", "991a58ad", "f4901f2e", "c6a33fa5", "9a13c872", "81f96d8c", "eca63237", "c902dd7f", "9547a52a", "89b6d080", "433b7784", "d02b855f", "5cf4bb33", "e8c80135", "fb53582e", "6d1da5db", "b5d4cd93", "7d810a18", "212d3420", "bea2a87b", "1a7e8890", "5a20c800", "71f5318a", "9d7cf9be", "47d60d99", "b18a0f54", "6be66188", "3ccdb7ea", "a39a31be", "97d7a328", "0de9601b", "f22041b5", "5d8fe79c", "2ca3b91e", "8d063218", "20ddd5b9", "39949030", "d45cbfda", "98225929", "7126ba6f", "632b40bd", "c1e2dabb", "b2463202", "2df7f8b8", "5770e2e9", "c1b3d9dd", "bac55b3d", "e863b5f2", "eb12db3f", "5312c679", "f9fca53e", "8f6c72cd", "6a6eed30", "567fac9d", "2fee1dfe", "6d0cd76a", "75e6cbd7", "a8ec71d6", "b1760c32", "125f0488", "c50d6ae6", "2f636346", "fb03331d", "1134a4d5", "9c6b2a09", "8a1f5c13", "dcfe0c7e", "23159a8a", "f1603221", "b6430444", "278cd472", "812b9819", "fe1ceb0b", "c28c8731", "ea57a186", "fc85fc86", "319089f6", "953b1b92", "20b10962", "94436810", "f3e7ec86", "e4ae1ec1", "3864ac4d", "9099f7ff", "eb9740e6", "82113ab1", "759fcc9b", "b805cbed", "456bc54b", "538fa191", "71bc9355", "7f51f33e", "ac200fc5", "964efdc9", "55c0c1c3", "16a8a60a", "acf9bfd9", "261329ba", "5209e362", "153c8661", "916a15c8", "2f22494d", "7b83a9d2", "78e4ded1", "1b891469", "11a8fc54", "02469fd7", "fdf8c151", "56c5ce8d", "19b501f6", "8376bfe2", "1fb94364", "c790ae7b", "caf7a244", "899cbe1b", "8d00c1d4", "d1a4be62", "a955323d", "0c36b083", "abef7485", "ee87ea44", "7703c370", "885cb17d", "f794b65b", "d4ad30e8", "826bc5a8", "4960ec86", "4cbc1c33", "34d96e3b", "bf8c40b0", "8df4cf6c", "092ddde9", "73f02e9d", "e7b0eb6a", "6a1cc3c3", "96bf54f4", "59a6369f", "6da2c8fa", "00a66247", "76a582e2", "7117702a", "a666148d", "7c89610d", "3fc276b6", "4314043b", "fb3585d7", "5eeb22e1", "161e3107", "17dc82c9", "644c670b", "f67124aa", "8d456799", "6a1abce5", "9e127a42", "04ba683b", "9f59939e", "09df08fd", "5ce658ef", "c5260ad5", "1b065882", "5d932fb3", "d77aed78", "396b0401", "cf2c1b53", "aedc32cf", "64948697", "b4d831fc", "55b6152b", "4abd4749", "bf35bfe3", "1fe03407", "a3c5f476", "016152a1", "147c95fb", "db9fca46", "5f775104", "d9845375", "b58fdd63", "b747a1a0", "01a0024a", "9473abd2", "5107cb1f", "17763604", "1915b13a", "1b051ae0", "5d0e3b9b", "15235cc5", "f86549cc", "bfbd1f2a", "e29d18a9", "8c93a5ce", "3f832f1b", "317f61f6", "cb990899", "742cbbb1", "d0c8e784", "3606597d", "f60c3dd5", "ac4ba3b4", "313e6329", "aa37baaa", "5e08c3fa", "429cf1a3", "6e306ad0", "eef57111", "71585d85", "73c46422", "8790aed4", "d26af547", "fc579208", "89f5570c", "bd00b19b", "9d264b47", "261e5371", "e080b2a0", "91bbf1fd", "a00993f5", "b6ce1a7e", "b1db82b0", "16b32aef", "c9800f16", "2ea04a7b", "7609e8de", "d6ab81b9", "4ea3a833", "9f50c039", "697b811c", "e217c38d", "95e76604", "87b45dd7", "fce886c4", "cdae36a1", "a9d1f6ff", "fc2fdf7a", "bb195b9e", "387a66fa", "ef3fe117", "531fb36b", "7524c9d6", "ebecacd0", "19544b1e", "b55e2da9", "243d34d7", "b8e5a4c3", "add65b4e", "0bfbeff8", "19a7cc69", "f96ec8de", "fede3dce", "2b43eb9f", "e79d8c6b", "abc9e2ef", "b92b595b", "ca60cf7a", "2b27271d", "56875570", "9b6e359c", "89df2d1f", "37525477", "7b2a65d3", "f258f692", "f552b9b9", "71dd65f7", "aab32a72", "9dcf61cc", "2caa3359", "7852d437", "e049b763", "37f2f078", "8c848aae", "b87b4bab", "dff632f1", "56df6e76", "76146752", "6171a0aa", "468fb796", "5c4c02de", "9426b1e0", "31079187", "46f741a3", "1e472aaf", "88eea8e0", "250e424c", "4eb07f37", "910c62d2", "4b86c160", "324aec12", "8fb18cf2", "3373280c", "abbe3ba3", "82190fa4", "55e11dfb", "120deabb", "7b49810b", "ecfc5f76", "d51af14f", "bc825d93", "83414286", "60a7eadb", "f5661c2e", "87101e36", "621352bc", "9109ba62", "6c62415e", "13efec26", "8900b405", "485e9247", "f0d9250e", "9feef3ea", "6089670c", "e45769ec", "8917a57d", "6b2f540e", "27409519", "67526fbc", "45961029", "705bae2a", "612a649b", "4c8ce765", "54d16966", "91180909", "701a8159", "23f6c70c", "26de90b7", "14b1b8fb", "2a090f2d", "5a95370c", "6d6869e2", "eb9da3ba", "84d07409", "986b37bb", "60e55973", "0bb33c14", "b762a170", "144fe77b", "12d9ce98", "ec180cc9", "2a993cb4", "21c0b478", "d4052253", "6762283c", "0730f173", "5b13c9b0", "6273c2da", "2457cdae", "b91a80c7", "e51d80ee", "be0b6998", "a0b5f180", "91fa0123", "ece79efe", "49082220", "50243637", "03df2762", "71445d69", "73d81789", "b9d7e716", "fc2b1652", "5aa52108", "6b75ded7", "ec3b55f5", "69318eff", "ee387e3d", "86e9d129", "6231e719", "5ef818e2", "95ecf616", "4a74d125", "0b6c9156", "d8fc1342", "682ea2b3", "6f769668", "65dc12fa", "7c7aa4db", "d3e83d43", "a075fd94", "94561e5e", "b8103bb7", "19676603", "5a9dadce", "40b84f16", "db4b3b67", "f4cb8de4", "601f5db2", "0974f112", "3908dc2e", "be12a64c", "29a2a75f", "a4838ff6", "295e5704", "2faf45c9", "e1e226cc", "618987f4", "3f14041f", "78521318", "d2c06d7d", "d8967a91", "a29cdfd5", "45edc3e2", "2f00e950", "be2ed9a4", "96c2287e", "7b86c681", "af4a4a43", "53aa57e6", "d2c718b2", "af643ffb", "cb841f5f", "4a386b96", "38ecc884", "a732aeb1", "db3dde79", "6882358a", "69367020", "429d8055", "142b3d0b", "faa01ef5", "f4b96f36", "8ac5839d", "4b39e945", "8e9b6de1", "282f2cdb", "8157aefd", "4b00d823", "46d3f15e", "236ae060", "c2a74bd2", "8474403c", "8b41cfe7", "5b8b7dfa", "2f369434", "572b2a2e", "8c2b8ba1", "09c5a739", "34f23d21", "d9d0c984", "4f700fb1", "8f84af4b", "a5990540", "94e976e1", "11ab33ba", "c1cea83b", "174f1087", "b6b2699d", "94b05377", "813b6ddd", "5a0ef819", "1b4f55ad", "13cc3595", "823a1e44", "a140f43a", "51248083", "152e2795", "50cc4571", "ff12c589", "70eadbb6", "4fa5311e", "7a0b9eaf", "8216cd24", "8d31ca3d", "b9f242ff", "23cb85af", "c4908d5d", "fe457c22", "880e3fdd", "f67f747d", "a950942f", "e6a3ea6b", "20c8cb89", "aed9d77e", "2875ceeb", "16f718e3", "9e806ab3", "954858a6", "ac875a98", "6d29b712", "e9af9f68", "c8ec261c", "9eb08477", "11984cf9", "4e1e3242", "80be4d77", "279bfce3", "6145cb63", "f032ac9d", "947162fb", "fc3b5937", "e70d0262", "76a60637", "5b8f54f1", "79f73dcd", "1ed0c0e0", "8808b3cf", "2161efea", "1a3d334d", "e4f29a35", "6106535a", "b0449c73", "e43c1a57", "dfc4d8a0", "67f4c44b", "c4060701", "59b55155", "693830fe", "135e550a", "2593ad14", "6899dded", "32ec077c", "1f0734f4", "848638da", "7b3da05a", "0a0f71e7", "6e5ad085", "3187290a", "1a9a647e", "927c294a", "835c934a", "82ceadf1", "a748ae27", "ea34c52c", "7089a04a", "c596a2b1", "b5dd29a9", "1012b1f9", "050dddb7", "7e3202dd", "44dd4a57", "d03efadf", "de758be0", "a9dc4fa7", "4fed06df", "0c97aa1b", "b429c2bb", "8aa380ab", "92dd4dcb", "9bd54259", "1b155577", "ab6f81c2", "a518c762", "001df1fe", "96820a03", "042fac3e", "e0a6efb8", "a4676d66", "a518a3b9", "f2651a7c", "6db09d45", "b42fa79c", "fdcf2e50", "7e5ec7a1", "1a5f7c49", "3fb74c49", "c6a6da11", "4dbf3df9", "a91069f8", "1878d811", "cebcb306", "c9478055", "279c5eb2", "99574c7d", "62d1c102", "1a32ee41", "b0495f15", "0d3a95ea", "c4f4ef8f", "b7071ebc", "4046d3b8", "7f3c9d9b", "1d80432a", "25444923", "a1b33390", "a4ec3a23", "051c2ed0", "d01f6f28", "8166e824", "1adf36c0", "8e26d3a5", "68191e20", "139c9710", "ebd80d03", "7bb67d3d", "7584d2cb", "5937483e", "0bfc534e", "2da58642", "dad5e0e7", "7c3df3cb", "df81afbd", "521a2e36", "55ab09b3", "88835226", "897517ca", "34204f22", "a4fcf982", "34738d9b", "d1626d46", "d0e94f4d", "c99aae72", "29ee052c", "26990929", "79a3fd98", "65b1aa53", "f83b7571", "64aadc3c", "79891eac", "62985939", "dc557e81", "405c12bd", "3923eaff", "9ccfee1b", "c073561b", "ffc82af0", "a843f480", "0cf96d2c", "80e4f0ba", "0d49b4e6", "64d53897", "6b263718", "3808c9cf", "fe873890", "7b9dae5c", "2f2f378c", "f63877ae", "a93faead", "a1362f16", "17a987c8", "18357297", "7a9343dc", "81186019", "48b3cc35", "f617d63b", "7099f511", "0e28ac97", "2266205b", "f551a288", "b240a6af", "ff90a587", "48ff0fe7", "0d9f901a", "c93c95ed", "39daffd6", "62ddcc3a", "0218b544", "c6ae2312", "3e67a604", "2270938c", "1228b88b", "ebdce9cc", "f69b4d50", "ec32c377", "364a1b36", "33cb6606", "6d7d6ed3", "c0df82b0", "80ed13eb", "ded8819e", "ea472c22", "3b197d0b", "adc508d5", "74bd4426", "f404f674", "6a724b6c", "0430f01c", "37daf645", "18a0ea17", "b132a345", "72dee45e", "5f30c1e0", "a3d6be29", "7553625a", "8d48a57f", "4e37e3cb", "c81512c1", "2a73693a", "cb5c08eb", "a0011ed4", "43bf4aeb", "d11a6a56", "e0c2849d", "88f1d219", "178779ab", "76cc8da9", "518982fb", "6660d27f", "25f27661", "65ee9fcf", "24690642", "2d95e6a4", "ef7970b3", "114d2509", "d9ded773", "eac3acec", "900cf71f", "8f577e5e", "57abcc31", "79516840", "d39156a5", "1489027a", "2d3f2f86", "be152b1a", "9f828b33", "848d2558", "838ae39d", "d3eaf349", "84a17d6f", "f53f7a05", "932f7fc4", "da4d4d91", "e4b52ede", "3e76541b", "6b2c338c", "dd2cc6cc", "b9d8c4ac", "6841094b", "e3ce5541", "cb822e5f", "4741de58", "c8b3b8f5", "38a3e400", "e4c37b28", "6daa47ed", "b36b41b0", "2f0d3052", "d9444fb6", "c1eff814", "29904ac9", "2490fc73", "14fdcca7", "23d59fe5", "88f3d2bd", "da1a7734", "61c5d74e", "1d0f032b", "1f54dce1", "0bf47ef2", "a27098be", "155763c0", "b637362e", "a2ea9973", "8d2b2768", "839c41a1", "720701a9", "461cc426", "e266cf88", "46f6caa2", "ee122115", "8b5f971a", "f7d2a59f", "21da8870", "d4b684f4", "17504c98", "acf1fcfe", "3929a082", "5ee12f71", "fb823950", "4a27e93b", "974fd3b5", "d718b6ae", "d6d8855d", "6c257617", "3b49c435", "5d799743", "5624effc", "420b853b", "2dae2b6e", "4d252382", "6173971d", "0f672804", "cd3e4e5f", "6ad11f30", "1cddfe58", "05f2b50c", "0f3efa90"])]
                          
    df_whey = df_whey.sample(18)
    CONF["index_name"] = INDEX_SUPPLEMENT_BRAZIL["index"]["whey"]
    data_ingestion(df_whey, CONF)

    message("set barrinha")
    keywords = WORDLIST["barrinha"]["subject"]
    blacklist = ["combo", "pack", "kit"]

    df_barrinha = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    df_barrinha = df_barrinha.sample(18)
    print(df_barrinha)
    CONF["index_name"] = INDEX_SUPPLEMENT_BRAZIL["index"]["bar"]
    data_ingestion(df_barrinha, CONF)

    message("set pretreino")
    keywords = WORDLIST["pretreino"]["subject"]
    beauty = WORDLIST["beauty"]["subject"]
    blacklist = ["combo", "pack", "kit", "brain"] + beauty

    df_pretreino = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    df_pretreino = df_pretreino.sample(18)
    print(df_pretreino)
    CONF["index_name"] = INDEX_SUPPLEMENT_BRAZIL["index"]["preworkout"]
    data_ingestion(df_pretreino, CONF)