"""
SITAC Integration Service
Handles authentication and protocolo submission to SITAC system
"""
import requests
import json
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)

class SITACService:
    """Service class for SITAC integration"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'SITAC_BASE_URL', 'https://crea-to.sitac.com.br/app/webservices')
        self.username = getattr(settings, 'SITAC_USERNAME', '')
        self.password = getattr(settings, 'SITAC_PASSWORD', '')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        })
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get basic authentication headers"""
        import base64
        
        # For basic auth, we just encode the raw credentials without URL encoding
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        return {'Authorization': f'Basic {encoded_credentials}'}
    
    def _get_bearer_headers(self, token: str) -> Dict[str, str]:
        """Get bearer token headers"""
        return {'Authorization': f'Bearer {token}'}
    
    def login(self) -> Tuple[bool, Optional[Dict]]:
        """
        Authenticate with SITAC and get access token
        Returns: (success, token_data)
        """
        try:
            url = f"{self.base_url}/auth/login"
            headers = self._get_auth_headers()
            
            # Debug logging
            logger.info(f"SITAC login attempt to: {url}")
            logger.info(f"Username: {self.username}")
            logger.info(f"Password length: {len(self.password)} characters")
            
            response = self.session.post(url, headers=headers, timeout=30)
            
            # Log response details for debugging
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 403:
                logger.error("SITAC returned 403 Forbidden - check credentials")
                return False, None
            
            response.raise_for_status()
            
            token_data = response.json()
            
            # Cache the token with expiration time
            expires_in = token_data.get('expires_in', 1800)
            cache_timeout = expires_in - 60  # Cache for 1 minute less than expiration
            cache.set('sitac_access_token', token_data, cache_timeout)
            
            logger.info("SITAC login successful")
            return True, token_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"SITAC login failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response content: {e.response.text}")
            return False, None
        except Exception as e:
            logger.error(f"Unexpected error during SITAC login: {str(e)}")
            return False, None
    
    def refresh_token(self, refresh_token: str) -> Tuple[bool, Optional[Dict]]:
        """
        Refresh access token using refresh token
        Returns: (success, token_data)
        """
        try:
            url = f"{self.base_url}/auth/refresh-token"
            headers = self._get_bearer_headers(refresh_token)
            
            response = self.session.post(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            token_data = response.json()
            
            # Cache the new token
            expires_in = token_data.get('expires_in', 1800)
            cache_timeout = expires_in - 60
            cache.set('sitac_access_token', token_data, cache_timeout)
            
            logger.info("SITAC token refresh successful")
            return True, token_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"SITAC token refresh failed: {str(e)}")
            return False, None
        except Exception as e:
            logger.error(f"Unexpected error during SITAC token refresh: {str(e)}")
            return False, None
    
    def get_valid_token(self) -> Optional[str]:
        """
        Get a valid access token, refreshing if necessary
        Returns: access_token or None
        """
        # Check cache first
        cached_token = cache.get('sitac_access_token')
        if cached_token and cached_token.get('access_token'):
            return cached_token['access_token']
        
        # Try to refresh if we have a refresh token
        if cached_token and cached_token.get('refresh_token'):
            success, new_token_data = self.refresh_token(cached_token['refresh_token'])
            if success and new_token_data.get('access_token'):
                return new_token_data['access_token']
        
        # If refresh fails, try to login
        success, token_data = self.login()
        if success and token_data.get('access_token'):
            return token_data['access_token']
        
        return None
    
    def submit_protocolo(self, protocolo_data: Dict) -> Tuple[bool, Optional[Dict]]:
        """
        Submit protocolo to SITAC
        Returns: (success, response_data)
        """
        try:
            # Get valid access token
            access_token = self.get_valid_token()
            if not access_token:
                logger.error("Could not obtain valid SITAC access token")
                return False, None
            
            url = f"{self.base_url}/protocolo/saveProtocolo"
            headers = self._get_bearer_headers(access_token)
            
            response = self.session.post(
                url,
                headers=headers,
                json=protocolo_data,
                timeout=30,
            )
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                # Log detailed diagnostics for 4xx/5xx
                logger.error(
                    "SITAC submission error %s: %s | payload=%s | response=%s",
                    response.status_code,
                    str(http_err),
                    json.dumps(protocolo_data, ensure_ascii=False),
                    response.text,
                )
                raise
            
            response_data = response.json()
            logger.info(f"SITAC protocolo submission successful: {response_data}")
            return True, response_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"SITAC protocolo submission failed: {str(e)}")
            return False, None
        except Exception as e:
            logger.error(f"Unexpected error during SITAC protocolo submission: {str(e)}")
            return False, None
    
    def create_protocolo_data(self, protocolo) -> Dict:
        """
        Create SITAC protocolo data from Django Protocolo model
        """
        # Determine tipo_pessoa based on protocolo type
        if protocolo.tipo == 'finalistico_pf':
            tipo_pessoa = 'profissional'
        elif protocolo.tipo == 'finalistico_pj':
            tipo_pessoa = 'empresa'
        else:
            # This method should not be used for administrativos submission,
            # but keep a safe default if called inadvertently.
            tipo_pessoa = 'profissional'

        # Format CPF/CNPJ (remove punctuation)
        cpf_cnpj = (
            protocolo.cpf_cnpj.replace('.', '').replace('-', '').replace('/', '')
            if protocolo.cpf_cnpj else ''
        )

        # Format date as DD/MM/YYYY
        data_emissao = protocolo.data_emissao.strftime('%d/%m/%Y')

        # Base description (Processo first)
        descricao_base = (
            f"Processo: n° {protocolo.numero}. "
            f"Cadastro de processo físico: ARMÁRIO-{protocolo.armario}, "
            f"PRATELEIRA-{protocolo.prateleira}, CAIXA {protocolo.caixa}"
        )

        # Append additional documents (Nome: Observação) if any
        documentos_extra = []
        for doc in getattr(protocolo, 'documentos', []).all():
            observacao = (doc.observacoes or '').strip()
            observacao_fmt = observacao if observacao else ''
            documentos_extra.append(
                f"{doc.tipo_documento.nome}: {observacao_fmt}".rstrip()
            )

        if documentos_extra:
            descricao = descricao_base + ". " + ", ".join(documentos_extra)
        else:
            descricao = descricao_base

        # Despacho entry (public), per provided example
        despacho_descricao = (
            f"Processo {protocolo.numero}. ARMÁRIO-{protocolo.armario}, "
            f"PRATELEIRA-{protocolo.prateleira}, CAIXA {protocolo.caixa}."
        )

        protocolo_data = {
            "interessados": [
                {
                    "tipo_pessoa": tipo_pessoa,
                    "cpfcnpj": cpf_cnpj,
                }
            ],
            "assunto": "COD04",
            "setor_origem": "3383",
            "setor_destino": "3383",
            "usuario_destino": "",
            "data_emissao": data_emissao,
            "descricao": descricao,
            "enviar_email_grupo_setor": False,
            "despachos": [
                {
                    "descricao": despacho_descricao,
                    "imprime_nova_pagina": False,
                    "disponivel_ambiente_publico": True,
                }
            ],
        }

        return protocolo_data
