import json

LAST_RULE_ID = "Rule 7-M"

class ExpertSystem:
    def __init__(self, rules_file):
        with open(rules_file, 'r') as f:
            self.rules = json.load(f)
        self.facts = {}
        self.history = []
        self.recommendations_made = set()  # Track recommendations made

    def apply_rule(self, rule):
        self.history.append(rule['id'])
        for action in rule['actions']:
            if 'Recommend' in action:
                recommendation = action['Recommend']

                if recommendation not in self.recommendations_made:
                    if 'Recommend' in self.facts:
                        self.facts['Recommend'].append(recommendation)
                    else:
                        self.facts['Recommend'] = [recommendation]

                    self.recommendations_made.add(recommendation)
                    print(f"Recommended music: {recommendation}")
                else:
                    print(f"Recommendation '{recommendation}' has already been made. Skipping to prevent loop.")
            elif 'Set' in action:
                for key, value in action['Set'].items():
                    if key in ['Tempo', 'Valence', 'Instrumentalness']:
                        self.facts['Task'] = 'Mapping'
                        if key in self.facts:
                            self.facts[key].append(value)
                        else:
                            self.facts[key] = [value]
                    elif key == 'Key':
                        if key in self.facts:
                            self.facts[key].extend(value)
                        else:
                            self.facts[key] = value
                    else:
                        self.facts[key] = value
            elif 'Mapping' and self.history[-1] == LAST_RULE_ID:
                break

    def forward_chain(self):
        applied = True
        while applied:
            applied = False
            for rule_set in self.rules.values():
                for rule in rule_set:
                    print(self.conditions_met(rule['condition']), rule['id'])
                    if self.conditions_met(rule['condition']) and rule['id'] not in self.history and LAST_RULE_ID not in self.history:
                        self.apply_rule(rule)
                        applied = True

    def conditions_met(self, condition):
        for key, value in condition.items():
            # Debug print to check the condition being evaluated
            print(f"Evaluating condition: {key} == {value}")
            
            if key == 'Facet':
                dominant_trait = self.facts.get("User's Personality Trait")
                if not dominant_trait:
                    print(f"Condition failed: No dominant trait found.")
                    return False
                facets = self.facts['Personality'].get(dominant_trait, {})
                if value not in facets:
                    print(f"Condition failed: Facet '{value}' not found in dominant trait '{dominant_trait}'.")
                    return False
                else:
                    print(f"Condition met: Facet '{value}' found in dominant trait '{dominant_trait}'.")
                    continue
            
            if key.endswith("Level"):
                facet_key = key.replace(" Level", "")
                dominant_trait = self.facts.get("User's Personality Trait")
                if not dominant_trait:
                    print(f"Condition failed: No dominant trait found.")
                    return False
                if self.facts['Personality'][dominant_trait].get(facet_key) != value:
                    print(f"Condition failed: Facet '{facet_key}' level '{value}' does not match.")
                    return False
                else:
                    print(f"Condition met: Facet '{facet_key}' level '{value}' matches.")
                    continue
            
            if key in ["User's Mood", "Submood"]:
                if self.facts.get(key) != value:
                    print(f"Condition failed: {key} '{value}' does not match current fact.")
                    return False
                else:
                    print(f"Condition met: {key} '{value}' matches.")
            
            if isinstance(value, list):
                if not any(r in self.facts.get('Recommend', []) for r in value):
                    print(f"Condition failed: None of the recommendations in {value} are found.")
                    return False
                else:
                    print(f"Condition met: Matching recommendations found in {value}.")
            
            elif value.startswith('NOT '):
                if self.facts.get(key) == value[4:]:
                    print(f"Condition failed: {key} should not be {value[4:]}")
                    return False
                else:
                    print(f"Condition met: {key} is not {value[4:]}")
            else:
                if self.facts.get(key) != value:
                    print(f"Condition failed: {key} is not {value}")
                    return False
                else:
                    print(f"Condition met: {key} matches {value}")
        
        return True

if __name__ == '__main__':
    es = ExpertSystem('rules.json')
    es.facts['Task'] = 'Begin'
    es.forward_chain()
    print("****************************")
    print("Recommended Query Parameters are as follows:")
    print(f"Key Signutures: {es.facts['Key']}")
    print(f"Tempo: {es.facts['Tempo']}")
    print(f"Valence: {es.facts['Valence']}")
    print(f"Instrumentalness: {es.facts['Instrumentalness']}")