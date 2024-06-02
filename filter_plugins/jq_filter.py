import jq

class FilterModule:
    def filters(self):
        return {
            'jq_filter': self.jq_filter
        }

    def jq_filter(self, data, expression):
        # Compile the jq filter expression
        compiled_expression = jq.compile(expression)

        # Apply the compiled filter to the input data
        filtered_data = compiled_expression.input(data).all()

        return filtered_data