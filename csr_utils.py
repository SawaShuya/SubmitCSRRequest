from cryptography import x509
from cryptography.hazmat.backends import default_backend

def read(csr_pem_string):
    print("Read CSR text")
    # CSRを解析
    csr_data = csr_pem_string.encode("utf-8")
    csr = x509.load_pem_x509_csr(csr_data, default_backend())
    
    # 各種情報を抽出
    subject = csr.subject
    subject_string = ", ".join([f"{attr.oid._name}={attr.value}" for attr in subject])

    print(f"Subject: {subject_string}")
    
    return subject_string
