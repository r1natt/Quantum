from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from .stas import test
import matplotlib.pyplot as plt

# Create your views here.

@csrf_exempt
def simulate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sim_time = float(data.get('sim_time', 150))
            cc_delay = float(data.get('cc_delay', 0.5))
            qc_atten = float(data.get('qc_atten', 3e-5))
            qc_dist = float(data.get('qc_dist', 5))

            # Run simulation and get figure
            fig = test(sim_time, cc_delay, qc_atten, qc_dist)

            # Convert figure to image
            canvas = FigureCanvas(fig)
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
            
            # Clean up
            plt.close(fig)
            buf.close()

            return HttpResponse(json.dumps({
                'status': 'success',
                'image': img_str
            }), content_type='application/json')

        except Exception as e:
            return HttpResponse(json.dumps({
                'status': 'error',
                'message': str(e)
            }), content_type='application/json', status=400)

    return HttpResponse(json.dumps({
        'status': 'error',
        'message': 'Only POST method is allowed'
    }), content_type='application/json', status=405)
