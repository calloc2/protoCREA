"""
Management command to test SITAC integration
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from protocolos.sitac_service import SITACService
from protocolos.models import Protocolo
import json

class Command(BaseCommand):
    help = 'Test SITAC integration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--protocolo-id',
            type=int,
            help='ID of protocolo to test with SITAC',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing SITAC integration...'))
        
        # Check if credentials are configured
        if not settings.SITAC_USERNAME or not settings.SITAC_PASSWORD:
            self.stdout.write(
                self.style.ERROR('SITAC credentials not configured. Please set SITAC_USERNAME and SITAC_PASSWORD in your .env file.')
            )
            return
        
        # Show credential info (without revealing password)
        self.stdout.write(f'Username: {settings.SITAC_USERNAME}')
        self.stdout.write(f'Password length: {len(settings.SITAC_PASSWORD)} characters')
        self.stdout.write(f'Password contains special chars: {any(c in settings.SITAC_PASSWORD for c in "()[]{}!@#$%^&*")}')
        self.stdout.write(f'Base URL: {settings.SITAC_BASE_URL}')
        
        sitac_service = SITACService()
        
        # Test authentication
        self.stdout.write('Testing authentication...')
        success, token_data = sitac_service.login()
        
        if success:
            self.stdout.write(self.style.SUCCESS('✓ Authentication successful'))
            self.stdout.write(f'Access token: {token_data.get("access_token", "N/A")[:20]}...')
            self.stdout.write(f'Expires in: {token_data.get("expires_in", "N/A")} seconds')
        else:
            self.stdout.write(self.style.ERROR('✗ Authentication failed'))
            return
        
        # Test with a protocolo if ID is provided
        protocolo_id = options.get('protocolo_id')
        if protocolo_id:
            try:
                protocolo = Protocolo.objects.get(id=protocolo_id)
                self.stdout.write(f'Testing with protocolo: {protocolo.numero}')
                
                # Create protocolo data
                protocolo_data = sitac_service.create_protocolo_data(protocolo)
                self.stdout.write('Protocolo data to be sent:')
                self.stdout.write(json.dumps(protocolo_data, indent=2, ensure_ascii=False))
                
                # Submit to SITAC
                success, response = sitac_service.submit_protocolo(protocolo_data)
                
                if success:
                    self.stdout.write(self.style.SUCCESS('✓ Protocolo submission successful'))
                    self.stdout.write(f'Response: {json.dumps(response, indent=2, ensure_ascii=False)}')
                else:
                    self.stdout.write(self.style.ERROR('✗ Protocolo submission failed'))
                    
            except Protocolo.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Protocolo with ID {protocolo_id} not found'))
        else:
            self.stdout.write('No protocolo ID provided. Use --protocolo-id to test with a specific protocolo.')
        
        self.stdout.write(self.style.SUCCESS('SITAC integration test completed.'))
