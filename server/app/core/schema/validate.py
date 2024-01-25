import re
from pydantic import EmailStr, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exception import UnprocessableEntity
from app.core.exception import BadRequestException


class Security:
    @staticmethod
    def ssrf_protection(value, field_name, errors, nullable=False):
        if value is None:
            return errors
        pattern = r"^[^'>/{()}\\<'\|&&\\]*(\\.[^'>/{()}\\<'\|&&\\]*)*$"
        regex = re.compile(pattern)

        if not regex.match(value):
            if field_name in errors:
                errors[field_name].append("Security error in data content")
            else:
                errors[field_name] = ["Security error in data content"]

        return errors


class Email:
    @staticmethod
    def validate_email(email, field_name, errors, nullable=False):
        if nullable and email is None:
            return errors
        try:
            email_str = EmailStr()
            if not email_str.validate(email):
                if field_name in errors:
                    errors[field_name].append("Email is invalid")
                else:
                    errors[field_name] = ["Email is invalid"]
        except:
            if field_name in errors:
                errors[field_name].append("Email is invalid")
            else:
                errors[field_name] = ["Email is invalid"]
        return errors


class Password:
    @staticmethod
    def contain_special_characters(password, field_name, errors, nullable=False):
        if nullable and password is None:
            return errors
        if not re.search(r"[^a-zA-Z0-9]", password):
            if field_name in errors:
                errors[field_name].append("Password must contain special characters")
            else:
                errors[field_name] = ["Password must contain special characters"]
        return errors

    @staticmethod
    def contain_numbers(password, field_name, errors):
        if not re.search(r"[0-9]", password):
            if field_name in errors:
                errors[field_name].append("Password must contain numbers")
            else:
                errors[field_name] = ["Password must contain numbers"]

        return errors

    @staticmethod
    def contain_uppercase(password, field_name, errors):
        if not re.search(r"[A-Z]", password):
            if field_name in errors:
                errors[field_name].append("Password must contain uppercase letters")
            else:
                errors[field_name] = ["Password must contain uppercase letters"]

        return errors

    @staticmethod
    def contain_lowercase(password, field_name, errors):
        if not re.search(r"[a-z]", password):
            if field_name in errors:
                errors[field_name].append("Password must contain lowercase letters")
            else:
                errors[field_name] = ["Password must contain lowercase letters"]

        return errors

    @staticmethod
    def min_length(password, length, field_name, errors):
        if not len(password) > length:
            if field_name in errors:
                errors[field_name].append(
                    f"Password must be at least {length} characters"
                )
            else:
                errors[field_name] = [f"Password must be at least {length} characters"]
        return errors

    @staticmethod
    def match(password, confirm_password, field_name, errors):
        if password != confirm_password:
            if field_name in errors:
                errors[field_name].append("Password not match")
            else:
                errors[field_name] = ["Password not match"]
        return errors


class Validate:
    def __init__(self, errors=None):
        self.errors = errors if errors else {}

    async def validate(self, request_body, db: AsyncSession, *args, **kwargs):
        try:
            if hasattr(request_body, "custom_validations"):
                self.result = await request_body.custom_validations(
                    self.errors,
                    db,
                    *args,
                    **kwargs,
                )
            else:
                assert "Validation class for input request must have custom_validations"

        except ValidationError as e:
            for error in e.errors():
                loc = error["loc"][0]
                msg = error["msg"]
                if loc in self.errors:
                    self.errors[loc].append(msg)
                else:
                    self.errors[loc] = [msg]
        none_field_error = []
        if "none_field_error" in self.errors:
            none_field_error = self.errors["none_field_error"]
            del self.errors["none_field_error"]

        if self.errors:
            raise UnprocessableEntity(error=self.errors)

        if none_field_error:
            raise BadRequestException(error=none_field_error)

        return self.result
