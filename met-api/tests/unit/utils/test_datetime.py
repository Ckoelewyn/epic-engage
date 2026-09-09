# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the datetime helpers."""

from datetime import datetime, timedelta

from met_api.utils.datetime import legislative_timezone


def test_bc_pacific_time_is_utc_minus_seven_in_december():
    """Assert BC local time stays on UTC-7 in winter."""
    december = legislative_timezone().localize(datetime(2026, 12, 15, 12, 0, 0))

    assert december.utcoffset() == timedelta(hours=-7)
