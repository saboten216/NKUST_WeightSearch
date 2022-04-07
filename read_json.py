from operator import index
import pandas as pd

'''
讀取專業選修json檔
'''
select_data = './data_json/select.json'
df_select_json = pd.read_json(select_data)
result_df = df_select_json[["scr_selcode" , "scr_precnt" , "Encrypt_selcode" , "sub_name" , "scj_sub_percode","scj_mso" ]]
select_df = result_df.drop_duplicates()
result_df.set_index("scr_selcode" , inplace=True)
result_df.to_csv("select.csv")
print(result_df)

'''
讀取通識json檔
'''

select_data = './data_json/select2.json'
df_select_json = pd.read_json(select_data)
result_df = df_select_json[["scr_selcode" , "scr_precnt" , "Encrypt_selcode" , "sub_name" , "scj_sub_percode","scj_mso" ]]
select2_df = result_df.drop_duplicates()
result_df.set_index("scr_selcode" , inplace=True)
result_df.to_csv("select2.csv")
print(result_df)

'''
讀取體育json檔
'''
select_data = './data_json/physical.json'
df_select_json = pd.read_json(select_data)
result_df = df_select_json[["scr_selcode" , "scr_precnt" , "Encrypt_selcode" , "sub_name" , "scj_sub_percode","scj_mso" ]]
physical_df = result_df.drop_duplicates()
result_df.set_index("scr_selcode" , inplace=True)
result_df.to_csv("physical.csv")
print(result_df)

