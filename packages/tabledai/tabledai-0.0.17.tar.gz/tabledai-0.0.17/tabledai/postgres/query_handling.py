import logging
from decimal import Decimal

class QueryHandling:
    def query(self, query: str, generative: bool = False, n_retries: int = 2) -> dict:
        result = {'success': False, 'message': None, 'sql': None, 'data': None, 'generation': None}
        if n_retries < 0 or not isinstance(n_retries, int):
            logging.info("The number of retries must be an positive integer. Defaulting to 2 retries.")
            n_retries = 2
        
        error_message = None
        for i in range(n_retries + 1):
            if i > 0:
                retry_prompt = (
                    f"The user query was {query}. The SQL query generated from OpenAI in the first call was: '{sql}'. "
                    f"This SQL failed to execute due to the following error: '{error_message}'. "
                    "Please try again, taking into account the error message."
                )
                prompt = self._build_sql_prompt(query, starter_prompt=retry_prompt)
                logging.info(f"Retrying to generate SQL for query: '{query}'...")
            else:
                prompt = self._build_sql_prompt(query)
                logging.info(f"Generating SQL for query: '{query}'...")

            sql = self._sql_openai_call(prompt)
            if not sql:
                logging.error("Failed to generate SQL query, trying again.")
                error_message = "Failed to generate SQL query."
                continue
            else:
                db_result_dict = self._query_db(sql)
                if not db_result_dict.get('success'):
                    logging.error(f"Failed to execute SQL query, trying again.")
                    error_message = db_result_dict.get('data')
                    continue
                else:
                    result_df = db_result_dict.get('data')
                    if result_df.empty:
                        logging.info("Query returned no results.")
                        error_message = "Query returned no results."
                        continue
                    else:
                        logging.info("Query executed successfully.")
                        for col in result_df.columns:
                            if result_df[col].dtype == object and isinstance(result_df[col].iloc[0], Decimal):
                                result_df[col] = result_df[col].astype(float)
                        result['success'] = True
                        result['message'] = "Query executed successfully."
                        result['data'] = result_df.to_dict(orient='records')

                        if generative:
                            generative_prompt = self._build_generative_prompt(query, result_df)
                            result['generation'] = self._generative_openai_call(generative_prompt)
                        return result

        result['message'] = "Failed to execute query after retries."
        return result