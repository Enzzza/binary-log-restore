import argparse
from multiprocessing import Pool
from multiprocessing import cpu_count
import pandas as pd
from modules.dataframe import create_dataframe
from modules.schema import schema
from modules.base import engine
from sqlalchemy import text, inspect
from functools import partial

def main(num_cores, seed_number):
    with Pool() as pool:
        data = pd.concat(pool.map(partial(create_dataframe, seed_number), range(num_cores)))
        data.to_sql(name='employees', con=engine, if_exists='append', index=False, dtype=schema)
        if 'id' not in [col['name'] for col in inspect(engine).get_columns('employees')]:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE employees ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--num_cores', type=int, default=None, help='Number of CPU cores to use')
    parser.add_argument('--seed_number', type=int, default=None, help='Seed number for Faker')
    args = parser.parse_args()

    if args.num_cores is None:
        num_cores = cpu_count() - 1
    else:
        num_cores = args.num_cores

    if args.seed_number is None:
        seed_number = 100
    else:
        seed_number = args.seed_number
    main(num_cores, seed_number)
