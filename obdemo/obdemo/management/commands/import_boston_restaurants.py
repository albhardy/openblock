#   Copyright 2011 OpenPlans and contributors
#
#   This file is part of OpenBlock
#
#   OpenBlock is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   OpenBlock is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with OpenBlock.  If not, see <http://www.gnu.org/licenses/>.
#


from django.core.management.base import BaseCommand
from ebpub.utils.script_utils import die, makedirs, wget, unzip
import os

class Command(BaseCommand):
    help = 'Import Boston neighborhoods as ebpub.db.Locations.'

    def handle(self, *args, **options):
        from ebdata.scrapers.us.ma.boston.restaurants.retrieval import main
        main()