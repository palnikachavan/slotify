from flask import Blueprint, request, jsonify, g
from app.models import Slot
from app.utils.auth import user_required
from app.tenants.database_router import get_tenant_session
from app.models.slot_user import SlotUser

user_booking_bp = Blueprint('user_booking', __name__)

@user_booking_bp.route('/book-slot', methods=['POST'])
@user_required 
def book_slot():
    data = request.get_json()
    slot_id = data.get('slot_id')
    service_id = data.get('service_id')

    if not all([slot_id, service_id]):
        return jsonify({'error': 'Missing required fields'}), 400

    user_id = g.user_id
    tenant = g.tenant
    session = get_tenant_session(tenant.db_uri)

    try:
        slot = session.get(Slot, slot_id)
        if not slot:
            return jsonify({'error': 'Slot not found'}), 404

        if slot.is_booked:
            return jsonify({'error': 'Slot is already marked as booked'}), 409

        existing_booking = session.query(SlotUser).filter_by(user_id=user_id, slot_id=slot_id).first()
        if existing_booking:
            return jsonify({'error': 'Slot already booked by this user'}), 409

        slot_user = SlotUser(user_id=user_id, slot_id=slot_id, service_id=service_id)
        session.add(slot_user)

        slot.is_booked = True 
        session.commit()

        return jsonify({'message': 'Slot booked successfully'}), 201

    except Exception as e:
        session.rollback()
        return jsonify({'error': f'Booking failed: {str(e)}'}), 500

@user_booking_bp.route('/delete-slot', methods=['DELETE'])
@user_required 
def cancel_slot():
    data = request.get_json()
    slot_id = data.get('slot_id')

    if not slot_id:
        return jsonify({'error': 'slot_id is required'}), 400

    user_id = g.user_id
    tenant = g.tenant
    session = get_tenant_session(tenant.db_uri)

    try:
        booking = session.query(SlotUser).filter_by(user_id=user_id, slot_id=slot_id).first()
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        session.delete(booking)
        slot = session.get(Slot, slot_id)
        if slot:
            slot.is_booked = False

        session.commit()
        return jsonify({'message': 'Booking cancelled'}), 200

    except Exception as e:
        session.rollback()
        return jsonify({'error': f'Cancellation failed: {str(e)}'}), 500