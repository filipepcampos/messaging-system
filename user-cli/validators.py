from prompt_toolkit.validation import Validator, ValidationError


class PasswordValidator(Validator):
    def validate(self, document):
        text = document.text

        # TODO: Match rules here with backend
        N_CHARACTERS = 6
        if len(text) < N_CHARACTERS:
            raise ValidationError(
                message=f"Your password must be at least {N_CHARACTERS} long",
            )
