from flask import Blueprint, request, jsonify, g
from app.utils.auth import tenant_admin_required
from app.tenants.database_router import get_tenant_session
from app.models.service import Service
from app.models.slot import Slot

booking_bp = Blueprint('bookings', __name__)  

# services routes
@booking_bp.route('/services', methods=['POST'])
@tenant_admin_required 
def create_service():
    tenant = g.tenant
    session = get_tenant_session(tenant.db_uri)

    data = request.get_json()
    service = Service(
        name=data['service_name'],
        description=data.get('description') 
    )
    session.add(service)
    session.commit()

    return jsonify({'message': 'Service created'}), 201


@booking_bp.route('/services', methods=['GET'])
@tenant_admin_required 
def list_services():
    session = get_tenant_session(g.tenant.db_uri)
    services = session.query(Service).all()
    return jsonify([{"id": s.id, "name": s.name, "description": s.description} for s in services])


@booking_bp.route('/services/<int:service_id>', methods=['PUT'])
@tenant_admin_required 
def update_service(service_id):
    session = get_tenant_session(g.tenant.db_uri)
    service = session.query(Service).get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    data = request.get_json()
    service.name = data.get('name', service.name)
    service.description = data.get('description', service.description)
    session.commit()
    return jsonify({'message': 'Service updated'})


@booking_bp.route('/services/<int:service_id>', methods=['DELETE'])
@tenant_admin_required 
def delete_service(service_id):
    session = get_tenant_session(g.tenant.db_uri)
    service = session.query(Service).get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    session.delete(service)
    session.commit()
    return jsonify({'message': 'Service deleted'})


# slots routes
@booking_bp.route('/services/<int:service_id>/slots', methods=['POST'])
@tenant_admin_required 
def create_slot(service_id):
    data = request.get_json()
    session = get_tenant_session(g.tenant.db_uri)

    slot = Slot(
        service_id=service_id,
        start_time=data['start_time'],
        end_time=data['end_time'],
        is_booked=data.get('is_booked', False)
    )
    session.add(slot)
    session.commit()
    return jsonify({'message': 'Slot created', 'slot_id': slot.id})


@booking_bp.route('/services/<int:service_id>/slots', methods=['GET'])
@tenant_admin_required 
def list_slots(service_id):
    session = get_tenant_session(g.tenant.db_uri)
    slots = session.query(Slot).filter_by(service_id=service_id).all()
    return jsonify([
        {
            "id": s.id,
            "start_time": s.start_time.isoformat(),
            "end_time": s.end_time.isoformat(),
            "is_booked": s.is_booked
        } for s in slots
    ])


@booking_bp.route('/slots/<int:slot_id>', methods=['PUT'])
@tenant_admin_required 
def update_slot(slot_id):
    session = get_tenant_session(g.tenant.db_uri)
    slot = session.query(Slot).get(slot_id)
    if not slot:
        return jsonify({'error': 'Slot not found'}), 404

    data = request.get_json()
    slot.start_time = data.get('start_time', slot.start_time)
    slot.end_time = data.get('end_time', slot.end_time)
    slot.is_booked = data.get('is_booked', slot.is_booked)
    session.commit()
    return jsonify({'message': 'Slot updated'})


@booking_bp.route('/slots/<int:slot_id>', methods=['DELETE'])
@tenant_admin_required 
def delete_slot(slot_id):
    session = get_tenant_session(g.tenant.db_uri)
    slot = session.query(Slot).get(slot_id)
    if not slot:
        return jsonify({'error': 'Slot not found'}), 404
    session.delete(slot)
    session.commit()
    return jsonify({'message': 'Slot deleted'})
