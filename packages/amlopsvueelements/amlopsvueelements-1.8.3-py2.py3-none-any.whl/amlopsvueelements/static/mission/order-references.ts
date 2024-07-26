import Api from '@/services'
import type { IPaginatedResponse, ITypeReference } from '@/types/general.types'
import type {
  IFuelUnit,
  IMappedPerson,
  IOrganisation,
  IPerson,
  IService
} from '@/types/order/order-reference.types'
import type { IAircraft, IAircraftTypeEntity } from '@/types/order/aircraft.types'
import type { IAirport } from '@/types/order/airport.types'
import { getIsAdmin } from '@/helpers'
import type { IClient, IGroundHandler, IOperator, IOrderStatus, IOrderType } from '@/types/order/order.types'
import type { Nullable } from '@/types/generic.types'

class OrderReferenceService extends Api {
  async fetchOrderStatuses() {
    try {
      const { data } = await this.get<IOrderStatus[]>(`api/v1/orders/order_statuses/?search=`)
      return data
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchOrderTypes() {
    try {
      const { data } = await this.get<IOrderType[]>(`api/v1/orders/order_types/`)
      return data
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchOrganisations(search?: string) {
    try {
      const {
        data: { results: organisations }
      } = await this.get<IPaginatedResponse<IOrganisation[]>>('api/v1/admin/organisations/', {
        params: { search, 'page[size]': 999 }
      })
      return organisations
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchOrganisationPeople(organisationId: number) {
    try {
      if (!organisationId) return []
      const url = `api/v1/organisations/${organisationId}/people/`
      const { data } = await this.get<IPerson[]>(url);
      const mappedData = data.map((item) => ({
        ...item,
        display: `${item.details.full_name} (${item.jobs[0]!.job_title})`
      }));
      return mappedData
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchAircraftTypes(organisationId: number) {
    try {
      if (getIsAdmin() && !organisationId) return []
      const url = getIsAdmin()
        ? `api/v1/admin/organisation/${organisationId}/aircraft_types/`
        : `api/v1/organisation/aircraft_types/`
      const {
        data: { data }
      } = await this.get<{ data: IAircraftTypeEntity[] }>(url);
      const mappedData = data.map(el => {
        return {
          ...el,
          full_repr: `${el.attributes.manufacturer} ${el.attributes.model} (${el.attributes.designator})`
        }
      });
      return mappedData
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchAircrafts(organisationId: number) {
    try {
      if (!organisationId) return []
      const url = `api/v1/aircraft/`;
      const { data } = await this.get<IAircraft[]>(url, {
        params: {
          operator: organisationId,
        }
      })
      return data
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchAirportLocations(search?: string | number) {
    try {
      const {
        data: { results: airports }
      } = await this.get<IPaginatedResponse<IAirport[]>>('api/v1/organisations/', {
        params: {
          search,
          type: 8,
          optional_fields: 'country'
        }
      })
      return airports
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchFuelQuantityUnits() {
    try {
      const { data } = await this.get<IFuelUnit[]>('api/v1/uom/')
      return data
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchFuelCategories() {
    try {
      const { data } = await this.get<ITypeReference[]>('api/v1/fuel_categories/')
      return data
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchGroundHandlers(airportId: number) {
    try {
      const {
        data: { results: handlers }
      } = await this.get<IPaginatedResponse<IGroundHandler[]>>('api/v1/organisations/', {
        params: {
          type: 3,
          base_airport: airportId,
        }
      }
      )
      return handlers
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchClients() {
    try {
      const { data: { results: clients } } = await this.get<IPaginatedResponse<IClient[]>>('api/v1/organisations/',
        {
          params: {
            type_str: 'client',
            optional_fields: 'client_status_list'
          }
        }
      )
      return clients
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchOperators() {
    try {
      const { data: { results: operators } } = await this.get<IPaginatedResponse<IOperator[]>>('api/v1/organisations/',
        {
          params: {
            type_str: 'operator',
          }
        }
      )
      return operators
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchMissionTypes() {
    try {
      const { data } = await this.get<ITypeReference[]>('api/v1/admin/handling_requests/types/')
      return data
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchPersonTitles() {
    try {
      const { data } = await this.get<ITypeReference[]>('api/v1/person_titles/')
      return data
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchPersonRoles() {
    try {
      const { data } = await this.get<ITypeReference[]>('api/v1/person_roles/')
      return data
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async fetchServices(
    locationId?: string | number,
    organisationId?: string | number,
    codeName?: string
  ) {
    try {
      const { data } = await this.get<{ data: IService[] }>('api/v1/handling_services/', {
        params: { organisation_id: organisationId, location_id: locationId, codename: codeName }
      })
      // Filter for unusable services
      const filteredServices = data.data
        ?.filter((service) => {
          return !(
            service.attributes.is_dla &&
            !service.attributes.is_dla_visible_arrival &&
            !service.attributes.is_dla_visible_departure
          )
        })
        .map((service) => {
          return { ...service, id: Number(service.id) }
        })
      return filteredServices
    } catch (e: any) {
      throw new Error(e)
    }
  }
  async fetchMeta() {
    try {
      const { data } = await this.get('api/v1/meta/')
      return data
    } catch (e: any) {
      throw new Error(e)
    }
  }

  async addNewPerson(payload: Nullable<IMappedPerson>) {
    const { data } = await this.post<IMappedPerson>(`api/v1/people/`, payload)
    const mappedData = {
      ...data,
      display: `${data.details.first_name} ${data.details.last_name} (${data.jobs[0].job_title})`
    };
    return mappedData;
  }
}

export default new OrderReferenceService()
