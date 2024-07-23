import fitz
import os
import argparse

def extract_embedded_files(pdf_path, output_folder):
    # Check if the PDF file exists
    if not os.path.isfile(pdf_path):
        print(f"Error: The file '{pdf_path}' does not exist.")
        return

    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Extract embedded XML files
    for i in range(doc.embfile_count()):
        # Get the embedded file info
        file_info = doc.embfile_info(i)
        file_name = file_info["name"]

        # Extract the embedded file if it is an XML
        if file_name.endswith(".xml"):
            # Read the embedded file
            file_data = doc.embfile_get(i)

            # Ensure output directory exists
            os.makedirs(output_folder, exist_ok=True)

            # Save the extracted file
            output_path = os.path.join(output_folder, file_name)
            with open(output_path, "wb") as output_file:
                output_file.write(file_data)

            print(f"Extracted: {output_path}")

    # Create a new PDF without embedded files
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_pdf_path = os.path.join(output_folder, f"{base_name}_converted.pdf")
    doc_new = fitz.open()  # Create a new PDF
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        doc_new.insert_pdf(doc, from_page=page_num, to_page=page_num)

    doc_new.save(output_pdf_path)
    print(f"Normal PDF saved as: {output_pdf_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Extract embedded XML files from PDF/A-3 documents and create a normal PDF."
    )
    parser.add_argument("pdf_path", help="Path to the PDF/A-3 file.")
    parser.add_argument("output_folder", help="Folder to save the extracted XML files and normal PDF.")

    args = parser.parse_args()

    extract_embedded_files(args.pdf_path, args.output_folder)

if __name__ == "__main__":
    main()
