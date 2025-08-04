from flask import Flask, render_template, request, jsonify
import uuid
import time
import json
from datetime import datetime

app = Flask(__name__)

# In-memory storage for demo (use database in production)
pipelines = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run-pipeline', methods=['POST'])
def run_pipeline():
    data = request.json
    pipeline_id = str(uuid.uuid4())
    
    # Store pipeline info
    pipelines[pipeline_id] = {
        'id': pipeline_id,
        'platform': data.get('platform'),
        'audience': data.get('audience'),
        'product': data.get('product'),
        'status': 'running',
        'progress': 0,
        'stage': 'Initializing content strategy...',
        'logs': ['🌱 Starting content cultivation process...'],
        'created_at': datetime.now(),
        'eta': 45
    }
    
    return jsonify({'pipeline_id': pipeline_id})

@app.route('/api/pipeline-status/<pipeline_id>')
def pipeline_status(pipeline_id):
    if pipeline_id not in pipelines:
        return jsonify({'error': 'Pipeline not found'}), 404
    
    pipeline = pipelines[pipeline_id]
    
    # Simulate progress
    elapsed = (datetime.now() - pipeline['created_at']).seconds
    
    if elapsed < 10:
        pipeline['progress'] = min(25, elapsed * 2.5)
        pipeline['stage'] = 'Analyzing trending content...'
        pipeline['logs'].append(f'📊 Discovering {pipeline["platform"]} trends...')
    elif elapsed < 20:
        pipeline['progress'] = min(50, 25 + (elapsed - 10) * 2.5)
        pipeline['stage'] = 'Generating creative concepts...'
        pipeline['logs'].append(f'🎨 Creating content for {pipeline["audience"]}...')
    elif elapsed < 30:
        pipeline['progress'] = min(75, 50 + (elapsed - 20) * 2.5)
        pipeline['stage'] = 'Crafting engaging scripts...'
        pipeline['logs'].append(f'✍️ Writing scripts for {pipeline["product"]}...')
    elif elapsed < 40:
        pipeline['progress'] = min(95, 75 + (elapsed - 30) * 2)
        pipeline['stage'] = 'Optimizing for engagement...'
        pipeline['logs'].append('🚀 Finalizing content strategy...')
    else:
        pipeline['progress'] = 100
        pipeline['status'] = 'completed'
        pipeline['stage'] = 'Content strategy ready!'
        pipeline['logs'].append('🎉 Strategy cultivation complete!')
    
    pipeline['eta'] = max(0, 45 - elapsed)
    
    return jsonify(pipeline)

@app.route('/api/pipeline-result/<pipeline_id>')
def pipeline_result(pipeline_id):
    if pipeline_id not in pipelines:
        return jsonify({'error': 'Pipeline not found'}), 404
    
    # Mock results for demo
    result = {
        'success': True,
        'pipeline_id': pipeline_id,
        'execution_time': '42 seconds',
        'top_trend': {
            'name': 'Microsoft Productivity Hacks',
            'overallScore': 8.7
        },
        'content_scripts': [
            {
                'title': 'Teams Meeting Productivity Tips',
                'category': 'Educational',
                'hook': 'Stop wasting time in meetings with this one Microsoft Teams trick!',
                'hashtags': ['#MicrosoftTeams', '#Productivity', '#WorkHacks']
            },
            {
                'title': 'Office 365 Hidden Features',
                'category': 'Tutorial',
                'hook': 'You\'ve been using Office wrong this whole time!',
                'hashtags': ['#Office365', '#Tutorial', '#Microsoft']
            },
            {
                'title': 'Remote Work Made Easy',
                'category': 'Lifestyle',
                'hook': 'How Microsoft 365 transformed my work-from-home game',
                'hashtags': ['#RemoteWork', '#Microsoft365', '#WorkLifeBalance']
            }
        ]
    }
    
    return jsonify(result)

@app.route('/view-report/<pipeline_id>')
def view_report(pipeline_id):
    return f"<h1>📊 Executive Content Strategy Report</h1><p>Pipeline ID: {pipeline_id}</p><p>Detailed content strategy analytics and recommendations would be displayed here in a production environment.</p>"

@app.route('/download/<pipeline_id>/<report_type>')
def download_report(pipeline_id, report_type):
    return f"📥 Downloading {report_type} report for pipeline {pipeline_id}..."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
