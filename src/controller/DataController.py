def validate_file(file):

       if file.content_type not in ["text/plain", "application/pdf"]:
            return False, "Unsupported file type. Allowed types are: .txt, .pdf" 
       
       if file.size > 10 * 1024 * 1024:  # 10 MB
            return False, "File size exceeded. Maximum allowed size is: 10 MB"

       return True, "File uploaded successfully."