from ..exceptions.health_exception import HealthPolicyException

def is_user_policy_exists(user, policy_premium, health_policies):
    return health_policies.objects.filter(user=user, policy_premium=policy_premium).count() >0

def validate_dependents(policy_premium, dependents):
    if policy_premium and dependents:
        policy_type = policy_premium.policy.policy_type
        num_dependents = dependents.count()

        if policy_type == 'Individual':
            if num_dependents > 1:
                raise HealthPolicyException(f'dependents: Individual policy can only have self as dependent.')
            for dependent in dependents:
                if dependent.relation != 'Self':
                    raise HealthPolicyException('dependents: Individual policy can only have self as dependent.')

        elif policy_type == 'Family':
            if num_dependents > 4:
                raise HealthPolicyException('dependents: Family policy can have up to 4 members as dependents.')
            for dependent in dependents:
                if dependent.relation not in ['Self', 'Spouse', 'Child']:
                    raise HealthPolicyException('dependents: Family policy dependents must be self, spouse, 2 children.')

        elif policy_type == 'Senior':
            if num_dependents > 2:
                raise HealthPolicyException(f'dependents : Senior Citizens policy can have up to 2 members as dependents.')
            for dependent in dependents:
                if dependent.relation != 'Parent':
                    raise HealthPolicyException(f'dependents: Senior Citizens policy dependents must be Parent.')

