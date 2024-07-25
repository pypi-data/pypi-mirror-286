import logging
from decimal import Decimal

class QueryHandling:
    def query(self, query: str, generative: bool = False) -> dict:
        result = {'success': False, 'message': None, 'sql': None, 'data': None, 'generation': None}
        prompt = self._build_sql_prompt(query)
        logging.info(f"Generating SQL for query: '{query}'...")
        sql_llm_result = self._sql_openai_call(prompt)

        if not sql_llm_result:
            logging.error("Failed to generate SQL query, please try again.")
            result['message'] = "Failed to generate SQL query."
            return result

        if not sql_llm_result.get('in_domain'):
            logging.info("The query is not in domain or cannot be answered with the provided data.")
            result['message'] = "The query is not in domain."
            return result

        sql = sql_llm_result.get('sql')
        result['sql'] = sql
        logging.info(f"SQL query generated successfully.")

        db_result_dict = self._query_db(sql)
        if not db_result_dict.get('success'):
            # logging.info("SQL query failed to execute.")
            retry_prompt = (
                f"The user query was {query}. The SQL query generated from OpenAI in the first call was: '{sql}'. "
                f"This SQL failed to execute due to the following error: '{db_result_dict.get('data')}'. "
                "Please try again, taking into account the error message."
            )
            prompt = self._build_sql_prompt(query, starter_prompt=retry_prompt)
            # logging.info(f"Retrying to generate SQL for query: '{query}'...")
            sql_llm_result = self._sql_openai_call(prompt)
            sql = sql_llm_result.get('sql')
            
            if not sql:
                # logging.error("Failed to generate SQL query on retry.")
                result['message'] = "Failed to generate SQL query."
                return result

            result['sql'] = sql
            db_result_dict = self._query_db(sql)

        if not db_result_dict.get('success'):
            logging.error(f"Failed to execute SQL query: {db_result_dict.get('data')}")
            result['message'] = "Failed to execute SQL query."
            return result

        result_df = db_result_dict.get('data')
        if result_df.empty:
            logging.info("Query returned no results.")
            result['message'] = "Query returned no results."
            return result

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
