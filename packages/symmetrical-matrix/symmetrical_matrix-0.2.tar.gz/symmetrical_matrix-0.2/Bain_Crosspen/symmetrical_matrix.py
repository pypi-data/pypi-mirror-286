import pandas as pd
import os

def load_excel(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name, index_col=0)

def create_symmetrical_matrix(df):
    return df.reindex(df.index, axis=1)

def rank_diagonal(matrix):
    return matrix.apply(lambda x: x.nlargest(len(x)).index, axis=1)

def save_results(matrix, ranks, output_file_path):
    with pd.ExcelWriter(output_file_path) as writer:
        matrix.to_excel(writer, sheet_name='Symmetrical_Matrix')
        ranks.to_excel(writer, sheet_name='Diagonal_Ranks')

def process_file(file_path, sheet_name):
    df = load_excel(file_path, sheet_name)
    symmetrical_matrix = create_symmetrical_matrix(df)
    diagonal_ranks = rank_diagonal(symmetrical_matrix)
    directory = os.path.dirname(file_path)
    output_file_path = os.path.join(directory, 'Symmetrical_Cross_Purchase_Matrix.xlsx')
    save_results(symmetrical_matrix, diagonal_ranks, output_file_path)
    print(f"Results have been exported to {output_file_path}")
