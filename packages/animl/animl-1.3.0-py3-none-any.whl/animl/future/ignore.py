# NOT FOR PUBLISHING
def correct_datetime(manifest, file_col="Filepath"):
    '''
    Rewrite the FileModifyDate for files that had them overwritten by the OS

    Ars:
        - manifest (DataFrame): manifest containing original FileModifyDates
        - file_col (str): column in manifest containing filepaths to rewrite
    '''
    et = ExifToolHelper()
    # reconvert format
    manifest['FileMod_Converted'] = manifest['FileModifyDate'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").strftime("%Y:%m:%d %H:%M:%S"))
    for _, row in tqdm(manifest.iterrows()):
        original = row["FileMod_Converted"]

        et.set_tags([row[file_col]],
                    tags={"FileModifyDate": original},
                    params=["-P", "-overwrite_original"])
