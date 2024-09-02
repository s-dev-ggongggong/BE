import json,os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run import create_app
from models.agent import Agent
from extensions import db, session_scope

def load_agents(file_path):
    app = create_app()
    
    with app.app_context():
        # Open the JSON file and load the data
        with open(file_path, 'r') as file:
            agents_data = json.load(file)
        
        print(f"Loaded {len(agents_data)} agent records from file.")
        
        with session_scope() as session:
            for agent_data in agents_data:
                # Create a new Agent object for each record
                agent = Agent(
                    name=agent_data['name'],
                    value=agent_data['value'],
                    description=agent_data.get('description')  # Description is optional
                )
                # Add the Agent object to the session
                session.add(agent)
            
            # Commit the session to save the data to the database
            try:
                session.commit()
                print(f"Successfully inserted {len(agents_data)} agents into the database.")
            except Exception as e:
                session.rollback()
                print(f"Failed to insert agents into the database: {str(e)}")
    
    print("Data loading completed.")

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__),'..', 'static','agents.json')
    load_agents(file_path)
