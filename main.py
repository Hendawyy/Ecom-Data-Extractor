import StorePage as SP
import AmazonScrapper as SCP
import vars as v

# https://www.amazon.eg/s?rh=n%3A18018165031%2Cp_4%3AAdidas&language=en&ref=bl_sl_s_sh_web_18018165031
# https://www.amazon.eg/s?k=TV&rh=n%3A21832982031&ref=nb_sb_noss
# https://www.amazon.eg/s?me=A3ANZAWA7POJMD&language=en&marketplaceID=ARBP9OOSHTCHU
# https://www.amazon.eg/s?bbn=21832883031&rh=n%3A21832883031%2Cp_89%3ASAMSUNG&language=en&pf_rd_i=21832883031&pf_rd_m=A1ZVRGNO5AYLOV&pf_rd_p=2eb88713-dff6-4694-b086-70d6edf29557&pf_rd_r=M03FDK3SQQ179ACQYJ3N&pf_rd_s=merchandised-search-10&pf_rd_t=101&ref=s9_acss_bw_cg_Mobile_3a1_w
# URL="https://www.amazon.eg/s?rh=n%3A18018165031%2Cp_4%3AAdidas&language=en&ref=bl_sl_s_sh_web_18018165031"



SCP.scrape_amazon_search(v.URL)
