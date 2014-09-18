#    Copyright (C) 2014  Yubico AB
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from u2fserver.core.api import U2FServerApplication
from u2fserver.core.transactionmc import MemcachedStore
from u2fserver.core.transactiondb import DBStore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_application(settings):
    engine = create_engine(settings['db'], echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    if settings['mc']:
        memstore = MemcachedStore(settings['mc_hosts'])
    else:
        memstore = DBStore(session)

    return U2FServerApplication(session, memstore)