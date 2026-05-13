import os
index_name = "rag-app"

def delete_files_in_folder(folder_path, pc):
    if not os.path.exists(folder_path):
        return {"message": f"Folder {folder_path} does not exist"}

    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Delete all vectors but keep the index
        index = pc.Index(index_name)
        index.delete(delete_all=True)

        return {"message": "All files in folder and index data have been deleted"}
    except Exception as e:
        return {"message": f"Error while deleting files: {e}"}