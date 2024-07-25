#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Scanner Variables """

from regscale.core.app.utils.variables import RsVariableType, RsVariablesMeta


class ScannerVariables(metaclass=RsVariablesMeta):
    """
    Scanner Variables class to define class-level attributes with type annotations and examples
    """

    # Define class-level attributes with type annotations and examples
    issueCreation: RsVariableType(str, "PerAsset|Consolidated", required=False)  # type: ignore # noqa: F821
