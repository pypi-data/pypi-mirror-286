from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.util.docutils import SphinxDirective
import matplotlib.pyplot as plt
import os

from stacksim.Stack import Stack
import yaml

class StackDirective(SphinxDirective):
    has_content = True
    option_spec = {
        'baseAddress': directives.unchanged,
        'showAddresses': directives.flag,
    }


    def run(self):
        base_address = self.options.get('baseAddress', '0x0')
        show_addresses = 'showAddresses' in self.options

        stack = Stack()

        yamlText = '\n'.join(self.content)

        obj = yaml.safe_load(yamlText)
        stack.loadYaml(obj)


        if self.builder.name == 'html':
            html_content = generate_stack_html(stack, base_address, show_addresses)
            raw_html_node = nodes.raw('', html_content, format='html')
            return [raw_html_node]
        elif self.builder.name == 'latex':
            image_path = generate_stack_image(stack, base_address, show_addresses, self.env)
            image_node = nodes.image(uri=image_path)
            return [image_node]

def generate_stack_html(stack, base_address, show_addresses):
    css_styles = """
    <style>
        .stack-table {
            border-collapse: collapse;
            margin: auto;
            width: 50%;
        }
        .stack-table th, .stack-table td {
            border: 1px solid black;
            padding: 5px;
            text-align: center;
        }
        .stack-table th {
            background-color: #f2f2f2;
        }
    </style>
    """
    
    rows = []
    for index, item in enumerate(stack):
        address = f'{int(base_address, 16) + index * 4:#010x}'
        text = f'{address}: {item}' if show_addresses else item
        rows.append(f'<tr><td>{text}</td></tr>')
    
    html_content = f'''
    {css_styles}
    <table class="stack-table">
        {" ".join(rows)}
    </table>
    '''
    return html_content

def generate_stack_image(stack, base_address, show_addresses, env):
    fig, ax = plt.subplots()

    ax.axis('off')
    y_offset = 0.8

    for index, item in enumerate(stack):
        address = f'{int(base_address, 16) + index * 4:#010x}'
        text = f'{address}: {item}' if show_addresses else item
        ax.text(0.5, y_offset, text, horizontalalignment='center', verticalalignment='center', fontsize=12)
        y_offset -= 0.2

    image_path = os.path.join(env.app.outdir, 'stack_image.png')
    plt.savefig(image_path)
    plt.close(fig)
    
    return image_path

def setup(app):
    app.add_directive('stack', StackDirective)
