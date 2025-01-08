
import clr

from .exceptions import InvalidTemplateError, TemplateTypeError
from .enroll import Enroll


clr.AddReference('Suprema.UFMatcher')
clr.AddReference('System')
clr.AddReference('System.Windows.Forms')

from Suprema import UFMatcher


class TemplateType:
    SUPREMA = 2001
    ISO19794 = 2002
    ANSI378 = 2003


def match_enrolls(enroll_1, enroll_2, security_level=4):
    if not isinstance(enroll_1, Enroll):
        raise TypeError('Object enroll_1 is not an instance of bm.Enroll')
    elif not isinstance(enroll_2, Enroll):
        raise TypeError('Object enroll_2 is not an instance of bm.Enroll')
    elif not enroll_1.template:
        raise InvalidTemplateError('Object enroll_1 does\'nt '
                                   'have a valid template.')
    elif not enroll_2.template:
        raise InvalidTemplateError('Object enroll_2 does\'nt '
                                   'have a valid template.')
    elif enroll_1.template_type != enroll_2.template_type:
        raise TemplateTypeError('Both enroll objects should have '
                                'the same template type.')
    return match_templates(template_1=enroll_1.template,
                           template_2=enroll_2.template,
                           security_level=security_level,
                           template_type=enroll_1.template_type)


def match_templates(template_1, template_2, security_level=4,
                    template_type=TemplateType.ISO19794):
    if not template_1:
        raise InvalidTemplateError('Object template_1 is not a valid template.')
    if not template_2:
        raise InvalidTemplateError('Object template_2 is not a valid template.')
    if security_level < 1 or security_level > 7:
        raise ValueError('security_level should be between 1 and 7')
    if template_type not in (TemplateType.SUPREMA, TemplateType.ISO19794,
                             TemplateType.ANSI378):
        raise ValueError('Invalid template_type. '
                         'accepted values are 2001, 2002, and 2003 ')
    matcher = UFMatcher()
    matcher.SecurityLevel = security_level
    matcher.nTemplateType = template_type
    result = matcher.Verify(template_1, len(template_1), template_2,
                            len(template_2), False)
    return result[1]
