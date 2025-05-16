def forte_payout_rule(submissions, total_reward):
    """
    Simulate Forte's Rules Engine for top 3 payout: 50/30/20%
    submissions: list of dicts with 'agent', 'score', 'model_size'
    Returns: list of dicts with 'agent', 'share', 'model_size'
    """
    from collections import defaultdict
    by_category = defaultdict(list)
    for s in submissions:
        by_category[s['model_size']].append(s)
    payouts = []
    for category, subs in by_category.items():
        top3 = sorted(subs, key=lambda x: x['score'], reverse=True)[:3]
        shares = [0.5, 0.3, 0.2]
        for i, winner in enumerate(top3):
            payouts.append({
                'agent': winner['agent'],
                'share': total_reward * shares[i],
                'model_size': category
            })
    return payouts

# Example usage:
if __name__ == "__main__":
    submissions = [
        {'agent': '0xA', 'score': 95, 'model_size': 'small'},
        {'agent': '0xB', 'score': 90, 'model_size': 'small'},
        {'agent': '0xC', 'score': 85, 'model_size': 'small'},
        {'agent': '0xD', 'score': 80, 'model_size': 'small'},
        {'agent': '0xE', 'score': 99, 'model_size': 'large'},
        {'agent': '0xF', 'score': 97, 'model_size': 'large'},
        {'agent': '0xG', 'score': 96, 'model_size': 'large'},
    ]
    total_reward = 1000
    payouts = forte_payout_rule(submissions, total_reward)
    for p in payouts:
        print(f"Agent {p['agent']} in {p['model_size']} gets {p['share']} tokens") 