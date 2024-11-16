from sqlalchemy import create_engine

def save_to_db(df, db_url='postgresql://username:password@localhost:5432/salesdb'):
    """Save predicted sales data to a PostgreSQL database."""
    engine = create_engine(db_url)
    df.to_sql('predicted_sales', engine, if_exists='replace', index=False)
