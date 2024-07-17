from provider.generic.count_provider import StaticCountProvider
from provider.transition.next_state_provider import DistinctNextStateProvider
from provider.transition.transition_probability_provider import \
    DrawWithoutReplacementTransitionProbabilityProviderFactory

factory = DrawWithoutReplacementTransitionProbabilityProviderFactory(
                transition_indices_provider=
                DistinctNextStateProvider(
                    number_of_next_state_provider=StaticCountProvider(count=3)
                )
            )

print(factory.get(4).get_transition_probabilities())
print(factory.get(4).get_transition_probabilities())
print(factory.get(4).get_transition_probabilities())